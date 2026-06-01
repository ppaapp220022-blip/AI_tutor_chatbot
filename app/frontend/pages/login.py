import streamlit as st

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

# 이미 로그인된 경우
if 'access_token' in st.session_state:
    st.switch_page('pages/chat.py')

# 더미 데이터
DUMMY_USERS = {
    'user1': {'password': '1234', 'role': 'USER'},
    'admin': {'password': '1234', 'role': 'ADMIN'},
}

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
    if not login_id or not password:
        st.error('아이디와 비밀번호를 입력해주세요')
    elif login_id not in DUMMY_USERS or DUMMY_USERS[login_id]['password'] != password:
        st.error('아이디 또는 비밀번호가 일치하지 않습니다')
    else:
        st.session_state['access_token'] = 'dummy_token'
        st.session_state['login_id'] = login_id
        st.session_state['role'] = DUMMY_USERS[login_id]['role']
        if DUMMY_USERS[login_id]['role'] == 'ADMIN':
            st.switch_page('pages/admin.py')
        else:
            st.switch_page('pages/chat.py')

if signup_btn:
    st.switch_page('pages/signup.py')
