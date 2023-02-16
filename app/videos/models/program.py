from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .video import Video


class Program(models.Model):

    video = models.OneToOneField(Video, on_delete=models.CASCADE)

    channel_id = models.PositiveBigIntegerField(
        _("Channel ID"), null=True, blank=True,
    )

    program_id = models.PositiveBigIntegerField(
        _("Program ID"), null=True, blank=True,
    )

    start_at = models.DateTimeField(_("start at"), null=True, blank=True)

    end_at = models.DateTimeField(_("end at"), null=True, blank=True)

    class Meta:
        verbose_name = _("program")
        verbose_name_plural = _("programs")

    def __str__(self):
        return self.video

    def get_absolute_url(self):
        return reverse("video_detail", kwargs={"pk": self.video.pk})
