from typing import Any

from .http_client import FrontendApiError, request_api


def fetch_members(page: int = 1, size: int = 10) -> dict[str, Any]:
    # 관리자 회원 목록 조회
    payload = request_api("GET", "/admin/member", params={"page": page, "size": size})
    if not isinstance(payload, dict):
        raise FrontendApiError("회원 목록 응답 형식이 올바르지 않습니다.")
    return payload


def fetch_member(login_id: str) -> dict[str, Any]:
    # 관리자 회원 상세 조회
    payload = request_api("GET", f"/admin/member/{login_id}")
    if not isinstance(payload, dict):
        raise FrontendApiError("회원 정보 응답 형식이 올바르지 않습니다.")
    return payload


def fetch_member_chat_history(login_id: str, page: int = 1, size: int = 10) -> dict[str, Any]:
    # 관리자 회원 채팅 이력 조회
    payload = request_api(
        "GET",
        f"/admin/member/{login_id}/chat-history",
        params={"page": page, "size": size},
    )
    if not isinstance(payload, dict):
        raise FrontendApiError("채팅 이력 응답 형식이 올바르지 않습니다.")
    return payload


def set_member_active(user_idx: list[int], is_active: bool) -> dict[str, Any] | None:
    # 회원 활성화 상태 변경
    return request_api(
        "PUT",
        "/admin/member/activate",
        json={"user_idx": user_idx, "is_active": is_active},
    )
