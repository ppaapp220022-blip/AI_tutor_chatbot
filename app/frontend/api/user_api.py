from typing import Any

from .http_client import FrontendApiError, request_api


def fetch_current_user() -> dict[str, Any]:
    # 현재 사용자 조회
    payload = request_api("GET", "/users/me")
    if not isinstance(payload, dict):
        raise FrontendApiError("사용자 정보 응답 형식이 올바르지 않습니다.")
    return payload
