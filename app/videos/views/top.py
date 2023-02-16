from django.db.models.query import Prefetch
from django.views.generic import ListView

from ..models import Thumbnail, Video


class TopView(ListView):
    model = Video
    template_name = "top.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                'thumbnails',
                Thumbnail.objects.filter(timestamp=0),
            )
        )
