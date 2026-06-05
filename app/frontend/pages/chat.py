import streamlit as st

from app.frontend.chat.chat_api import FrontendApiError
from app.frontend.chat import init_chat_session_state, load_chat_rooms
from app.frontend.chat import apply_chat_styles
from app.frontend.chat import render_lobby_view, render_room_view, render_sidebar

PERSONAS = ["일반 튜터", "수학 전문가", "영어 전문가", "과학 전문가", "역사 전문가"]

def main() -> None:
    # 채팅 페이지 메인
    """Compose the chat page from smaller modules and keep the entry file lightweight."""
    st.set_page_config(
        page_title="AI Tutor Chatbot",
        page_icon="🤖",
        layout="wide",
    )
    apply_chat_styles()

    if "access_token" not in st.session_state:
        st.switch_page("pages/login.py")

    init_chat_session_state()

    try:
        load_chat_rooms()
    except FrontendApiError as exc:
        st.error(exc.message)

    render_sidebar(PERSONAS)

    if st.session_state["current_room"] is None:
        render_lobby_view(PERSONAS)
    else:
        render_room_view(PERSONAS)

main()
