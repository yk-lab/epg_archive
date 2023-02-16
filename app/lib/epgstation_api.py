import requests
from django.conf import settings


def bool_to_querystring(value: bool) -> str:
    return 'true' if value else 'false'


class EPGStationAPI:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or settings.EPGSTATION_API_ROOT

    def get_recorded_detail(self, recorded_id: int, is_half_width: bool):
        _is_half_width = bool_to_querystring(is_half_width)
        resp = requests.get(
            f'{self.base_url}/recorded/{recorded_id}',
            params={
                'isHalfWidth': _is_half_width,
            },
        )
        resp.raise_for_status()
        return resp.json()

    def get_thumbnails_detail(self, thumbnail_id: int, requests_kwargs={}):
        resp = requests.get(
            f'{self.base_url}/thumbnails/{thumbnail_id}',
            **requests_kwargs,
        )
        resp.raise_for_status()
        return resp

    def get_videos_detail(self, video_file_id: int, is_download: bool, requests_kwargs={}):  # noqa: E501
        _is_download = bool_to_querystring(is_download)
        resp = requests.get(
            f'{self.base_url}/videos/{video_file_id}',
            params={
                'isDownload': _is_download,
            },
            **requests_kwargs,
        )
        resp.raise_for_status()
        return resp
