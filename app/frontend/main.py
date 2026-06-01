import streamlit as st

st.set_page_config(
    page_title='AI Tutor Chatbot',
    page_icon='🤖',
    layout='centered'
)

# 로그인 여부 확인 후 리다이렉트
if 'access_token' not in st.session_state:
    st.switch_page('pages/login.py')
else:
    st.switch_page('pages/chat.py')
