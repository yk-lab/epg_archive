import boto3
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, UUIDModel

from ..utils import get_suffix_from_content_type
from .video import Video


class Thumbnail(TimeStampedModel, UUIDModel):

    video = models.ForeignKey(
        Video, verbose_name=_("Video"), on_delete=models.CASCADE,
        related_name='thumbnails'
    )

    timestamp = models.PositiveBigIntegerField(_("timestamp"))

    content_type = models.CharField(
        _('content type'),
        max_length=64,
        default='image/jpeg')

    class Meta:
        verbose_name = _("thumbnail")
        verbose_name_plural = _("thumbnails")

    def __str__(self):
        return f'{self.video}: {self.timestamp}'

    def get_key(self):
        suffix = get_suffix_from_content_type(self.content_type)
        return f'thumbnails/{self.id}{suffix}'

    def presigned_get_object_url(self):
        s3_client = boto3.client('s3', **settings.S3)
        return s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.S3_BUCKET_NAME,
                'Key': self.get_key(),
                'ResponseContentType': self.content_type,
            },
            ExpiresIn=180)
