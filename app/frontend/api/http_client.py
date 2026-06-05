import os
from typing import Any

import requests
import streamlit as st

API_BASE_URL = os.getenv("BACKEND_API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


class FrontendApiError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def extract_error_message(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return response.text or "요청 처리 중 오류가 발생했습니다."

    if isinstance(payload, dict):
        detail = payload.get("detail")
        if isinstance(detail, str) and detail.strip():
            return detail
        if isinstance(detail, list) and detail:
            messages: list[str] = []
            for item in detail:
                if isinstance(item, dict):
                    message = item.get("msg") or item.get("message")
                    if isinstance(message, str) and message.strip():
                        messages.append(message)
            if messages:
                return ", ".join(messages)

        for key in ("message", "detail", "error"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value
    return str(payload)


def auth_headers() -> dict[str, str]:
    # 세션 access 토큰 헤더 변환
    token = st.session_state.get("access_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def send_request(
    method: str,
    path: str,
    *,
    auth: bool = True,
    cookies: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
) -> requests.Response:
    # 인증 헤더 포함 요청
    headers = auth_headers() if auth else {}
    try:
        return requests.request(
            method=method,
            url=f"{API_BASE_URL}{path}",
            params=params,
            json=json,
            data=data,
            files=files,
            cookies=cookies,
            headers=headers,
            timeout=30,
        )
    except requests.RequestException as exc:
        raise FrontendApiError(f"백엔드 연결 실패: {exc}") from exc


def request_api(
    method: str,
    path: str,
    *,
    auth: bool = True,
    cookies: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
) -> Any:
    # 응답 에러 공통 처리
    response = send_request(
        method,
        path,
        auth=auth,
        cookies=cookies,
        params=params,
        json=json,
        data=data,
        files=files,
    )

    # access 만료 시 refresh 후 재시도
    if response.status_code == 401 and auth and path not in {"/users/refresh"}:
        try:
            from app.frontend.api.auth_api import refresh_access_token
        except Exception as exc:  # pragma: no cover - import wiring fallback
            raise FrontendApiError(f"인증 갱신 모듈을 불러오지 못했습니다: {exc}") from exc

        try:
            refresh_access_token()
        except FrontendApiError:
            raise FrontendApiError("인증이 만료되었습니다. 다시 로그인해주세요.")

        response = send_request(
            method,
            path,
            auth=auth,
            cookies=cookies,
            params=params,
            json=json,
            data=data,
            files=files,
        )

    # 에러 메시지 변환
    if response.status_code >= 400:
        raise FrontendApiError(extract_error_message(response))

    # 본문 없으면 None 반환
    if response.status_code == 204 or not response.content:
        return None
    return response.json()
