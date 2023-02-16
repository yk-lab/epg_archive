from logging import getLogger

import boto3
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, UUIDModel

logger = getLogger(__name__)


class Video(TimeStampedModel, UUIDModel):

    title = models.CharField(_("title"), max_length=512)

    description = models.TextField(_("description"), blank=True, default='')

    extended = models.TextField(_("extended"), blank=True, default='')

    genre1 = models.PositiveSmallIntegerField(
        _("genre1"), null=True, blank=True,
    )

    sub_genre1 = models.PositiveSmallIntegerField(
        _("sub genre1"), null=True, blank=True,
    )

    genre2 = models.PositiveSmallIntegerField(
        _("genre2"), null=True, blank=True,
    )

    sub_genre2 = models.PositiveSmallIntegerField(
        _("sub genre2"), null=True, blank=True,
    )

    genre3 = models.PositiveSmallIntegerField(
        _("genre3"), null=True, blank=True,
    )

    sub_genre3 = models.PositiveSmallIntegerField(
        _("sub genre3"), null=True, blank=True,
    )

    video_type = models.CharField(_("video type"), max_length=50)

    video_size = models.PositiveBigIntegerField(_("video size"))

    class Meta:
        verbose_name = _("video")
        verbose_name_plural = _("videos")

    def __str__(self):
        return self.title

    @property
    def suffix(self):
        if self.video_type == 'H.264':
            return '.mp4'
        raise NotImplementedError

    def get_key(self):
        return f'videos/{self.id}{self.suffix}'

    def presigned_get_object_url(self):
        s3_client = boto3.client('s3', **settings.S3)
        meta = s3_client.head_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=self.get_key(),
        )

        return s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.S3_BUCKET_NAME,
                'Key': self.get_key(),
                'ResponseContentType': meta.get('ContentType'),
            },
            ExpiresIn=3600)
