import streamlit as st

st.set_page_config(
    page_title='AI Tutor Chatbot',
    page_icon='🤖',
    layout='centered'
)

# 로그인 상태에 따른 진입 페이지 분기
if 'access_token' not in st.session_state:
    st.switch_page('pages/login.py')
else:
    # 관리자면 관리자 페이지 이동
    if st.session_state.get('role') == 'ADMIN':
        st.switch_page('pages/admin.py')
    else:
        # 일반 사용자는 채팅 페이지 이동
        st.switch_page('pages/chat.py')
