from typing import Any

import streamlit as st

from .chat_state import handle_send_message

def render_chat_composer(room_id: int) -> None:
    # 하단 고정 입력창에서 파일 업로드, 메시지 입력, 전송 버튼을 렌더링
    with st.container(key="chat-composer"):
        with st.form("chat_compose_form", clear_on_submit=True):
            upload_col, input_col, send_col = st.columns([1.5, 6.9, 1.6])
            with upload_col:
                uploaded_file = st.file_uploader(
                    "파일 업로드",
                    label_visibility="collapsed",
                    key=f"file_upload_{st.session_state['file_uploader_key']}",
                )
            with input_col:
                prompt = st.text_input(
                    "메시지",
                    placeholder="메시지를 입력하세요",
                    label_visibility="collapsed",
                )
            with send_col:
                send_clicked = st.form_submit_button("전송", use_container_width=True)

        if send_clicked:
            _submit_prompt(room_id, prompt, uploaded_file)

        if uploaded_file:
            st.markdown(
                f'<div class="composer-file-name"><span class="composer-file-label">첨부 파일</span><span class="composer-file-value">{uploaded_file.name}</span></div>',
                unsafe_allow_html=True,
            )


def _submit_prompt(room_id: int, prompt: str, uploaded_file: Any | None) -> None:
    # 빈 입력을 막고 실제 전송 처리를 상태 로직에 적용
    if not prompt or not prompt.strip():
        st.warning("메시지를 입력해주세요.")
        return
    handle_send_message(room_id, prompt.strip(), uploaded_file)
