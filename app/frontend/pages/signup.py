import streamlit as st

from app.frontend.api.auth_api import send_otp_email, signup_user, verify_otp_email
from app.frontend.api.http_client import FrontendApiError

st.set_page_config(
    page_title='회원가입',
    page_icon='🤖',
    layout='centered'
)

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    div.stButton > button {
        border-radius: 8px;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        opacity: 0.85;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# 이미 로그인된 경우 역할별 이동
if 'access_token' in st.session_state:
    if st.session_state.get('role') == 'ADMIN':
        st.switch_page('pages/admin.py')
    else:
        st.switch_page('pages/chat.py')

# 회원가입 플래그 기본값
if 'otp_sent' not in st.session_state:
    st.session_state['otp_sent'] = False
if 'otp_verified' not in st.session_state:
    st.session_state['otp_verified'] = False
if 'signup_info' not in st.session_state:
    st.session_state['signup_info'] = {}


@st.dialog('이메일 인증')
def otp_modal():
    st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
            <span>인증코드를 입력해주세요</span>
        </div>
    """, unsafe_allow_html=True)
    st.info(f"{st.session_state['signup_info'].get('email', '')} 로 인증코드를 발송했습니다")
    st.write('')
    otp_code = st.text_input('인증코드', placeholder='인증코드 6자리를 입력하세요')
    st.write('')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('인증 확인', use_container_width=True, type='primary'):
            if not otp_code:
                st.error('인증코드를 입력해주세요')
            else:
                try:
                    verify_otp_email(st.session_state['signup_info'].get('email', ''), otp_code)
                except FrontendApiError as exc:
                    st.error(exc.message)
                else:
                    st.session_state['otp_verified'] = True
                    st.rerun()
    with col2:
        if st.button('취소', use_container_width=True):
            st.session_state['otp_sent'] = False
            st.rerun()


# 타이틀
st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
        <h2 style="margin:0">AI Tutor Chatbot</h2>
    </div>
    <p style="color:#888; margin-bottom:8px">회원가입</p>
""", unsafe_allow_html=True)
st.divider()

with st.form('signup_form'):
    login_id = st.text_input('아이디', placeholder='아이디를 입력하세요 (30자 이내)')
    password = st.text_input('비밀번호', type='password', placeholder='비밀번호를 입력하세요')
    password_check = st.text_input('비밀번호 확인', type='password', placeholder='비밀번호를 다시 입력하세요')
    email = st.text_input('이메일', placeholder='이메일을 입력하세요')
    st.write('')

    col1, col2 = st.columns(2)
    with col1:
        # 인증 완료시 버튼 disable
        otp_btn = st.form_submit_button(
            '✓ 인증 완료' if st.session_state['otp_verified'] else '인증코드 발송',
            use_container_width=True,
            type='primary',
            disabled=st.session_state['otp_verified']
        )
    with col2:
        back_btn = st.form_submit_button('로그인으로 돌아가기', use_container_width=True)

    # 인증 완료시 회원가입 버튼 폼 안에 표시
    if st.session_state['otp_verified']:
        st.divider()
        signup_submit_btn = st.form_submit_button('회원가입 완료', use_container_width=True, type='primary')
    else:
        signup_submit_btn = False

if otp_btn:
    # 입력값 검증 후 인증번호 발송
    if not login_id or not password or not password_check or not email:
        st.error('모든 항목을 입력해주세요')
    elif password != password_check:
        st.error('비밀번호가 일치하지 않습니다')
    else:
        try:
            send_otp_email(email)
        except FrontendApiError as exc:
            st.error(exc.message)
        else:
            st.session_state['otp_sent'] = True
            st.session_state['signup_info'] = {
                'login_id': login_id,
                'password': password,
                'password_check': password_check,
                'email': email
            }
            st.rerun()

if signup_submit_btn:
    # 인증 완료 정보로 회원가입
    info = st.session_state.get('signup_info', {})
    if not info.get('login_id') or not info.get('password'):
        st.error('모든 항목을 입력해주세요')
    elif info.get('password') != info.get('password_check'):
        st.error('비밀번호가 일치하지 않습니다')
    else:
        try:
            signup_user(
                info['login_id'],
                info['password'],
                info['email'],
            )
        except FrontendApiError as exc:
            st.error(exc.message)
        else:
            st.success('회원가입이 완료됐습니다')
            st.session_state['otp_sent'] = False
            st.session_state['otp_verified'] = False
            st.session_state['signup_info'] = {}
            st.switch_page('pages/login.py')

if back_btn:
    st.switch_page('pages/login.py')

if st.session_state['otp_sent'] and not st.session_state['otp_verified']:
    otp_modal()
