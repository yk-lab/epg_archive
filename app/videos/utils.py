import mimetypes

from requests import Response


def get_suffix_from_resp_header(resp: Response):
    content_type = resp.headers.get('content-type')
    if not content_type:
        raise NotImplementedError
    return get_suffix_from_content_type(content_type)


def get_suffix_from_content_type(content_type: str):
    for k, v in mimetypes.types_map.items():
        if v == content_type:
            return k
    raise NotImplementedError
