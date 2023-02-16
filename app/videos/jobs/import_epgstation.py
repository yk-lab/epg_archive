from __future__ import annotations

import json
from logging import getLogger

from django.core.management import call_command
from django_rq import job

logger = getLogger(__name__)


@job('default', timeout=3600)
def import_epgstation(recorded_id: int, thumbnail_id: int, video_file_id: int):
    try:
        call_command(
            'import_epgstation', recorded_id, thumbnail_id, video_file_id)
    except Exception as e:
        logger.exception(e)
        return json.dumps({
            'is_success': False,
            'result': str(e),
        })
    else:
        return json.dumps({
            'is_success': True,
        })
