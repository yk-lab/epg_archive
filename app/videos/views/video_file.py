from typing import Any

from django.views.generic import DetailView, RedirectView

from ..models import Video


class VideoFileView(RedirectView, DetailView):
    model = Video

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        return self.get_object().presigned_get_object_url()
