from typing import Any

from .http_client import FrontendApiError, request_api


def fetch_current_user() -> dict[str, Any]:
    # 현재 사용자 조회
    payload = request_api("GET", "/users/me")
    if not isinstance(payload, dict):
        raise FrontendApiError("사용자 정보 응답 형식이 올바르지 않습니다.")
    return payload


def update_user(login_id: str, password: str, email: str) -> dict[str, Any]:
    # 회원 정보 수정
    payload = request_api("PUT", "/users/modify", json={
        "login_id": login_id,
        "password": password,
        "email": email,
    })
    if not isinstance(payload, dict):
        raise FrontendApiError("회원 정보 수정 응답 형식이 올바르지 않습니다.")
    return payload


def withdraw_user() -> None:
    # 회원 탈퇴
    request_api("DELETE", "/users/withdraw")
