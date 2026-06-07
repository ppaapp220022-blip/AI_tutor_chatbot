import streamlit as st

from app.frontend.api.auth_api import send_otp_email, verify_otp_email
from app.frontend.api.http_client import FrontendApiError
from app.frontend.api.user_api import fetch_current_user, update_user, withdraw_user

st.set_page_config(
    page_title='마이페이지',
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

if 'access_token' not in st.session_state:
    st.switch_page('pages/login.py')

# 이메일 OTP 세션 초기화
if 'email_otp_sent' not in st.session_state:
    st.session_state['email_otp_sent'] = False
if 'email_otp_verified' not in st.session_state:
    st.session_state['email_otp_verified'] = False
if 'new_email_pending' not in st.session_state:
    st.session_state['new_email_pending'] = ''


# OTP 검증 모달
@st.dialog('이메일 인증')
def otp_verify_modal() -> None:
    st.info(f"{st.session_state['new_email_pending']} 으로 인증코드를 발송했습니다")
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
                    verify_otp_email(st.session_state['new_email_pending'], otp_code)
                    st.session_state['email_otp_verified'] = True
                    st.rerun()
                except FrontendApiError as e:
                    st.error(e.message)
    with col2:
        if st.button('취소', use_container_width=True):
            st.session_state['email_otp_sent'] = False
            st.session_state['new_email_pending'] = ''
            st.rerun()


@st.dialog('회원 탈퇴')
def withdraw_modal() -> None:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f38ba8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            <strong>정말 탈퇴하시겠습니까?</strong>
        </div>
        <p style="color:#888; font-size:13px">탈퇴 시 모든 데이터가 삭제되며 복구가 불가능합니다</p>
    """, unsafe_allow_html=True)
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('탈퇴하기', use_container_width=True, type='primary'):
            try:
                withdraw_user()
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.switch_page('pages/login.py')
            except FrontendApiError as e:
                st.error(e.message)
    with col2:
        if st.button('취소', use_container_width=True):
            st.rerun()


# 헤더
st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/></svg>
        <h2 style="margin:0">마이페이지</h2>
    </div>
""", unsafe_allow_html=True)
st.divider()

# 현재 정보 조회
try:
    user = fetch_current_user()
except FrontendApiError as e:
    st.error(e.message)
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.write(f"**아이디:** {user.get('login_id', '')}")
with col2:
    st.write(f"**이메일:** {user.get('email', '')}")
    st.write(f"**권한:** {user.get('role', '')}")

st.divider()

# 회원 정보 수정 - 탭으로 분리
st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        <strong>회원 정보 수정</strong>
    </div>
""", unsafe_allow_html=True)

tab_pw, tab_email = st.tabs(['🔒 비밀번호 변경', '📧 이메일 변경'])

# 비밀번호 변경 탭
with tab_pw:
    with st.form('pw_form'):
        new_password = st.text_input('새 비밀번호', type='password', placeholder='변경할 비밀번호를 입력하세요')
        st.write('')
        pw_btn = st.form_submit_button('변경하기', use_container_width=True, type='primary')

    if pw_btn:
        if not new_password:
            st.error('새 비밀번호를 입력해주세요')
        else:
            try:
                update_user(
                    login_id=user.get('login_id', ''),
                    password=new_password,
                    email=user.get('email', '')
                )
                st.success('비밀번호가 변경됐습니다')
            except FrontendApiError as e:
                st.error(e.message)

# 이메일 변경 탭
with tab_email:
    with st.form('email_form'):
        new_email = st.text_input('새 이메일', placeholder='변경할 이메일을 입력하세요')
        st.write('')
        col1, col2 = st.columns(2)
        with col1:
            otp_btn = st.form_submit_button(
                '✓ 인증 완료' if st.session_state['email_otp_verified'] else '인증코드 발송',
                use_container_width=True,
                type='primary',
                disabled=st.session_state['email_otp_verified']
            )
        with col2:
            email_btn = st.form_submit_button(
                '변경하기',
                use_container_width=True,
                disabled=not st.session_state['email_otp_verified']
            )

    if otp_btn:
        if not new_email:
            st.error('변경할 이메일을 입력해주세요')
        else:
            try:
                send_otp_email(new_email)
                st.session_state['new_email_pending'] = new_email
                st.session_state['email_otp_sent'] = True
                st.session_state['email_otp_verified'] = False
            except FrontendApiError as e:
                st.error(e.message)

    if email_btn:
        try:
            update_user(
                login_id=user.get('login_id', ''),
                password=user.get('password', ''),
                email=st.session_state['new_email_pending']
            )
            st.success('이메일이 변경됐습니다')
            st.session_state['email_otp_sent'] = False
            st.session_state['email_otp_verified'] = False
            st.session_state['new_email_pending'] = ''
        except FrontendApiError as e:
            st.error(e.message)

    if st.session_state['email_otp_sent'] and not st.session_state['email_otp_verified']:
        otp_verify_modal()

st.write('')
if st.button('← 채팅으로 돌아가기', use_container_width=True):
    st.switch_page('pages/chat.py')

st.divider()

# 회원 탈퇴
st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f38ba8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        <strong style="color:#f38ba8">회원 탈퇴</strong>
    </div>
""", unsafe_allow_html=True)

if st.button('탈퇴하기', use_container_width=True):
    withdraw_modal()
