import streamlit as st

from app.frontend.api.auth_api import login_user
from app.frontend.api.http_client import FrontendApiError
from app.frontend.api.user_api import fetch_current_user

st.set_page_config(
    page_title='로그인',
    page_icon='🤖',
    layout='centered'
)

# 네비게이션바 숨기기
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# 이미 로그인된 경우 역할별 이동
if 'access_token' in st.session_state:
    if st.session_state.get('role') == 'ADMIN':
        st.switch_page('pages/admin.py')
    else:
        st.switch_page('pages/chat.py')

# 로그인 실패 메시지 세션 보관
if 'login_error_message' not in st.session_state:
    st.session_state['login_error_message'] = ''


@st.dialog('로그인 실패')
def login_error_modal() -> None:
    st.error(st.session_state.get('login_error_message', ''))
    if st.button('확인', use_container_width=True, type='primary'):
        st.session_state['login_error_message'] = ''
        st.rerun()

st.title('🤖 AI Tutor Chatbot')
st.subheader('로그인')
st.divider()

with st.form('login_form'):
    login_id = st.text_input('아이디', placeholder='아이디를 입력하세요')
    password = st.text_input('비밀번호', type='password', placeholder='비밀번호를 입력하세요')
    st.write('')

    col1, col2 = st.columns(2)
    with col1:
        login_btn = st.form_submit_button('로그인', use_container_width=True)
    with col2:
        signup_btn = st.form_submit_button('회원가입', use_container_width=True)

if login_btn:
    # 필수 입력값 누락 안내
    if not login_id or not password:
        st.session_state['login_error_message'] = '아이디와 비밀번호를 입력해주세요'
        st.rerun()
    else:
        # 로그인 성공 시 access 토큰 저장
        try:
            login_payload, refresh_token = login_user(login_id, password)
            st.session_state['access_token'] = login_payload['access_token']
            profile = fetch_current_user()
        except FrontendApiError as exc:
            # 실패 시 세션 초기화
            for key in ('access_token', 'refresh_token', 'login_id', 'member_id', 'role'):
                st.session_state.pop(key, None)
            st.session_state['login_error_message'] = exc.message or '로그인에 실패했습니다.'
            st.rerun()
        else:
            # 로그인 성공 후 사용자 정보 저장
            st.session_state['refresh_token'] = refresh_token
            st.session_state['login_id'] = profile.get('login_id', login_id)
            st.session_state['member_id'] = profile.get('id')
            st.session_state['role'] = profile.get('role', 'USER')
            st.session_state['login_error_message'] = ''
            # 역할별 진입 화면 분기
            if st.session_state['role'] == 'ADMIN':
                st.switch_page('pages/admin.py')
            else:
                st.switch_page('pages/chat.py')

if signup_btn:
    st.switch_page('pages/signup.py')

if st.session_state.get('login_error_message'):
    login_error_modal()
