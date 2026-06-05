from typing import Any

import streamlit as st

from .chat_api import FrontendApiError, create_chat_room, delete_chat_room
from .chat_state import get_member_id_for_new_room, load_chat_rooms, load_messages


@st.dialog("새 채팅방 만들기")
def create_room_modal(personas: list[str]) -> None:
    # 새 채팅방 생성에 필요한 입력값을 받고 생성 후 목록/메시지를 갱신한다.
    """Render the create-room modal and create a room when the form is submitted."""
    room_title = st.text_input("채팅방 이름", placeholder="채팅방 이름을 입력하세요")
    persona = st.selectbox("페르소나 선택", personas)
    default_member_id = get_member_id_for_new_room() or 1

    if st.session_state.get("member_id"):
        member_id = st.session_state["member_id"]
        st.caption(f"회원 ID: {member_id}")
    else:
        member_id = int(
            st.number_input(
                "회원 ID",
                min_value=1,
                value=default_member_id,
                step=1,
                help="로그인 연동 전이라 채팅방 생성에 필요한 회원 ID를 직접 입력해야 합니다.",
            )
        )

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("만들기", use_container_width=True, type="primary"):
            if not room_title.strip():
                st.error("채팅방 이름을 입력해주세요")
            else:
                try:
                    created_room = create_chat_room(member_id, room_title.strip(), persona)
                    st.session_state["member_id"] = member_id
                    load_chat_rooms(select_room_id=created_room["id"])
                    load_messages(created_room["id"])
                    st.rerun()
                except FrontendApiError as exc:
                    st.error(exc.message)
    with col2:
        if st.button("취소", use_container_width=True):
            st.rerun()


@st.dialog("채팅방 나가기")
def leave_room_modal(room: dict[str, Any]) -> None:
    # 채팅방 삭제 여부를 확인하고 확정 시 현재 상태까지 함께 정리한다.
    """Render the delete-room modal and remove the selected room on confirmation."""
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f38ba8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            <strong>'{room['title']}'</strong> 채팅방을 나가시겠습니까?
        </div>
        <p style="color:#888; font-size:13px">채팅방을 나가면 실제 백엔드 데이터에서도 삭제됩니다</p>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("나가기", use_container_width=True, type="primary"):
            try:
                delete_chat_room(room["id"])
                deleted_current_room = (
                    st.session_state["current_room"]
                    and st.session_state["current_room"]["id"] == room["id"]
                )
                load_chat_rooms()
                if deleted_current_room:
                    st.session_state["current_room"] = None
                    st.session_state["messages"] = []
                st.rerun()
            except FrontendApiError as exc:
                st.error(exc.message)
    with col2:
        if st.button("취소", use_container_width=True):
            st.rerun()
