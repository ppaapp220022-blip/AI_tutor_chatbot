from typing import Any

import streamlit as st

from .http_client import FrontendApiError, request_api, send_request, extract_error_message


def login_user(login_id: str, password: str) -> tuple[dict[str, Any], str | None]:
    # 로그인 요청
    response = send_request(
        "POST",
        "/users/login",
        auth=False,
        json={"login_id": login_id, "password": password},
    )
    if response.status_code >= 400:
        raise FrontendApiError(extract_error_message(response))
    if not response.content:
        raise FrontendApiError("로그인 응답이 비어 있습니다.")
    return response.json(), response.cookies.get("refresh_token")


def send_otp_email(email: str) -> dict[str, Any] | None:
    # 인증번호 메일 발송
    return request_api("POST", "/users/send-otp", auth=False, json={"email": email})


def verify_otp_email(email: str, otp_code: str) -> dict[str, Any] | None:
    # 인증번호 검증
    return request_api(
        "POST",
        "/users/verify-otp",
        auth=False,
        json={"email": email, "otp_code": otp_code},
    )


def signup_user(login_id: str, password: str, email: str) -> dict[str, Any] | None:
    # 회원가입 요청
    return request_api(
        "POST",
        "/users/signup",
        auth=False,
        json={"login_id": login_id, "password": password, "email": email},
    )


def refresh_access_token() -> str:
    # refresh 토큰으로 access 재발급
    refresh_token = st.session_state.get("refresh_token")
    if not refresh_token:
        raise FrontendApiError("로그인이 만료되었습니다. 다시 로그인해주세요.")

    response = send_request(
        "POST",
        "/users/refresh",
        auth=False,
        cookies={"refresh_token": refresh_token},
    )
    if response.status_code >= 400:
        raise FrontendApiError(extract_error_message(response))
    if not response.content:
        raise FrontendApiError("토큰 재발급 응답이 비어 있습니다.")

    payload = response.json()
    access_token = payload.get("access_token")
    if not access_token:
        raise FrontendApiError("토큰 재발급 응답이 올바르지 않습니다.")

    st.session_state["access_token"] = access_token
    if payload.get("token_type"):
        st.session_state["token_type"] = payload["token_type"]
    return access_token


def logout_user() -> None:
    # 서버 로그아웃 처리
    request_api("POST", "/users/logout")
