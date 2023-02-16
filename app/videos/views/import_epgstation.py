from logging import getLogger

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from ..forms import ImportEPGStationForm
from ..jobs import import_epgstation

logger = getLogger(__name__)

_FormT = ImportEPGStationForm


class ImportEPGStationFormView(FormView):
    form_class = ImportEPGStationForm
    initial = {
        'is_half_width': False,
    }

    success_url = reverse_lazy('import_epgstation')

    template_name = 'videos/import_epgstation.html'

    def form_valid(self, form: _FormT) -> HttpResponse:
        resp = super().form_valid(form)
        import_epgstation.delay(
            form.api_response['id'],
            form.thumbnail_id,
            form.video_file['id'],
        )
        messages.success(
            self.request,
            f'{form.api_response["name"]} の取り込みを開始しました')
        return resp
