from logging import getLogger
from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import gettext_lazy as _
from lib.epgstation_api import EPGStationAPI
from requests.exceptions import HTTPError

logger = getLogger(__name__)


class ImportEPGStationForm(forms.Form):
    recorded_id = forms.IntegerField(
        label=_('Recorded ID'),
    )
    is_half_width = forms.BooleanField(
        label=_('Is half width'),
        required=False,
    )

    @property
    def helper(self):
        helper = FormHelper()
        helper.add_input(Submit('submit', '取り込む', css_class='btn-primary'))
        return helper

    def clean(self) -> dict[str, Any]:
        data = super().clean()

        if recorded_id := data.get('recorded_id'):
            api = EPGStationAPI()
            try:
                self.api_response = api.get_recorded_detail(
                    recorded_id,
                    data['is_half_width'],
                )
            except HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    raise forms.ValidationError('指定された ID の録画データは見つかりませんでした')
                raise
            else:
                self.video_file = self.api_response['videoFiles'][0]

                thumbnails = self.api_response.get('thumbnails') or []
                if len(thumbnails) == 0:
                    raise forms.ValidationError('指定された ID のサムネイルが見つかりませんでした')
                self.thumbnail_id = thumbnails[0]

                if not self.video_file:
                    raise forms.ValidationError('指定された ID の動画ファイルは見つかりませんでした')

                if self.api_response['isRecording']:
                    raise forms.ValidationError('録画中のため取り込みできません')

        return data
