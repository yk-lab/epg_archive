import json
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from typing import Any

import boto3
from boto3.s3.transfer import TransferConfig
from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction
from lib.epgstation_api import EPGStationAPI

from ...models import Program, Thumbnail, Video
from ...utils import get_suffix_from_resp_header

logger = getLogger(__name__)


@dataclass
class VideoFileData:
    id: int
    name: str
    filename: str
    type: str
    size: int


def include_thumbnail_id(resp: dict[str, Any], thumbnail_id: int):
    return thumbnail_id in resp.get('thumbnails', []) or []


def get_video_date(resp: dict[str, Any], video_file_id: int):
    video_files_data = resp.get('videoFiles', []) or []

    data: dict[str, Any]
    for data in video_files_data:
        if data['id'] == video_file_id:
            return VideoFileData(**data)
    return None


class Command(BaseCommand):
    help = "Import video from EPGStation."

    def add_arguments(self, parser):
        parser.add_argument('recorded_id', type=int)
        parser.add_argument('thumbnail_id', type=int)
        parser.add_argument('video_file_id', type=int)

    def handle(self, *args, **options):
        s3 = boto3.client('s3', **settings.S3)

        epgstationz_api = EPGStationAPI()
        recorded = epgstationz_api.get_recorded_detail(options['recorded_id'], False)  # noqa: E501

        if recorded['isRecording']:
            raise CommandError('録画中のため取り込めません')

        if recorded['isEncoding']:
            raise CommandError('エンコード中のため取り込めません')

        if not include_thumbnail_id(recorded, options['thumbnail_id']):
            raise CommandError('不正なサムネイルIDです')

        video_file_data = get_video_date(recorded, options['video_file_id'])
        if not video_file_data:
            raise CommandError('不正なビデオIDです')

        thumbnail_file = epgstationz_api.get_thumbnails_detail(
            options['thumbnail_id'],
            requests_kwargs={
                'stream': True,
            },
        )
        video_file = epgstationz_api.get_videos_detail(
            options['video_file_id'],
            False,
            requests_kwargs={
                'stream': True,
            },
        )

        s3_transfer_config = TransferConfig(
            max_concurrency=1,
        )
        with transaction.atomic():
            video = Video()
            program = Program(video=video)
            thumbnail = Thumbnail(video=video)

            video.title = recorded.get('name')
            video.description = recorded.get('description') or ''
            video.extended = recorded.get('extended') or ''
            video.genre1 = recorded.get('genre1')
            video.sub_genre1 = recorded.get('subGenre1')
            video.genre2 = recorded.get('genre2')
            video.sub_genre2 = recorded.get('subGenre2')
            video.genre3 = recorded.get('genre3')
            video.sub_genre3 = recorded.get('subGenre3')
            video.video_type = video_file_data.name
            video.video_size = video_file_data.size

            program.channel_id = recorded.get('channelId')
            program.program_id = recorded.get('programId')
            start_at = datetime.fromtimestamp(s_at / 1000)\
                if (s_at := recorded.get('startAt')) else None
            end_at = datetime.fromtimestamp(e_at / 1000)\
                if (e_at := recorded.get('endAt')) else None
            program.start_at = start_at if start_at else None
            program.end_at = end_at if end_at else None

            thumbnail.timestamp = 0

            video.full_clean()
            program.full_clean(exclude=['video'])
            thumbnail.full_clean(exclude=['video'])

            s3.upload_fileobj(
                video_file.raw,
                settings.S3_BUCKET_NAME,
                f'videos/{video.id}{get_suffix_from_resp_header(video_file)}',
                ExtraArgs={
                    'ContentType': video_file.headers.get('content-type'),
                },
                Config=s3_transfer_config,
            )

            s3.put_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=f'videos/{video.id}.json',
                Body=json.dumps(recorded),
                ContentType='application/json',
            )

            s3.upload_fileobj(
                thumbnail_file.raw,
                settings.S3_BUCKET_NAME,
                f'thumbnails/{thumbnail.id}{get_suffix_from_resp_header(thumbnail_file)}',  # noqa: E501
                ExtraArgs={
                    'ContentType': thumbnail_file.headers.get('content-type'),
                },
            )

            video.save()
            program.save()
            thumbnail.save()
