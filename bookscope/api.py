from typing import Any, Dict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


def _build_error_payload(
    *,
    code: str,
    message: str,
    details: Any = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return response

    default_code = getattr(exc, "default_code", "api_error")

    if response.status_code == 400:
        response.data = _build_error_payload(
            code=str(default_code),
            message="Validation failed.",
            details=response.data,
        )
        return response

    detail = response.data.get("detail") if isinstance(response.data, dict) else None
    if isinstance(detail, list):
        detail = " ".join(str(item) for item in detail)

    response.data = _build_error_payload(
        code=str(default_code),
        message=str(detail or "Request could not be completed."),
    )
    return response


class HealthCheckResponse(Response):
    def __init__(self, **kwargs):
        super().__init__({"status": "ok", "service": "bookscope-api"}, **kwargs)
