import streamlit as st

from app.frontend.api.http_client import FrontendApiError
from app.frontend.chat import init_chat_session_state, load_chat_rooms, load_personas
from app.frontend.chat import apply_chat_styles
from app.frontend.chat import render_lobby_view, render_room_view, render_sidebar

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
        load_personas()
        load_chat_rooms()
    except FrontendApiError as exc:
        st.error(exc.message)

    personas = st.session_state.get("personas", [])
    if not personas:
        st.warning("사용 가능한 페르소나 목록을 불러오지 못했습니다.")
        st.stop()
    render_sidebar(personas)

    if st.session_state["current_room"] is None:
        render_lobby_view(personas)
    else:
        render_room_view(personas)

main()
