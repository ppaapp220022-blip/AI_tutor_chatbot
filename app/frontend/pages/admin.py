import streamlit as st

st.set_page_config(
    page_title='관리자',
    page_icon='🤖',
    layout='wide'
)

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }

    [data-testid="stSidebar"] {
        background-color: #1e1e2e;
    }
    [data-testid="stSidebar"] * {
        color: #cdd6f4 !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background-color: #313244;
        color: #cdd6f4 !important;
        border: 1px solid #45475a;
        border-radius: 8px;
        width: 100%;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #45475a !important;
        border-color: #585b70 !important;
    }
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

DUMMY_USERS = [
    {'id': 1, 'login_id': 'user1', 'email': 'user1@test.com', 'role': 'USER', 'is_active': True},
    {'id': 2, 'login_id': 'user2', 'email': 'user2@test.com', 'role': 'USER', 'is_active': True},
    {'id': 3, 'login_id': 'user3', 'email': 'user3@test.com', 'role': 'USER', 'is_active': False},
]

if 'users' not in st.session_state:
    st.session_state['users'] = DUMMY_USERS
if 'selected_user' not in st.session_state:
    st.session_state['selected_user'] = None

# 사이드바
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#cdd6f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
            <span style="font-size:16px; font-weight:600; color:#cdd6f4">관리자</span>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    if st.button('채팅으로 이동', use_container_width=True):
        st.switch_page('pages/chat.py')
    st.write('')
    if st.button('로그아웃', use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page('pages/login.py')

# 회원 상세 조회
if st.session_state['selected_user'] is not None:
    user = st.session_state['selected_user']

    if st.button('← 목록으로 돌아가기'):
        st.session_state['selected_user'] = None
        st.rerun()

    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin:16px 0 8px">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/></svg>
            <h2 style="margin:0">{user['login_id']} 회원 상세 정보</h2>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**아이디:** {user['login_id']}")
        st.write(f"**이메일:** {user['email']}")
    with col2:
        st.write(f"**권한:** {user['role']}")
        if user['is_active']:
            st.markdown("""
                <div style="display:flex; align-items:center; gap:6px">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#a6e3a1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>
                    <span style="color:#a6e3a1">활성</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="display:flex; align-items:center; gap:6px">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f38ba8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg>
                    <span style="color:#f38ba8">비활성</span>
                </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <strong>채팅 이력</strong>
        </div>
    """, unsafe_allow_html=True)
    st.info('백엔드 연동 후 채팅 이력이 표시됩니다')

# 회원 목록
else:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
            <h2 style="margin:0">관리자 페이지</h2>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <strong>전체 회원 목록</strong>
        </div>
    """, unsafe_allow_html=True)

    selected_ids = []

    col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 1])
    with col1: st.write('**선택**')
    with col2: st.write('**아이디**')
    with col3: st.write('**이메일**')
    with col4: st.write('**상태**')
    with col5: st.write('**상세**')
    st.divider()

    for user in st.session_state['users']:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 1])
        with col1:
            checked = st.checkbox('', key=f"check_{user['id']}")
            if checked:
                selected_ids.append(user['id'])
        with col2:
            st.write(user['login_id'])
        with col3:
            st.write(user['email'])
        with col4:
            if user['is_active']:
                st.markdown("""<div style="display:flex;align-items:center;gap:6px"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#a6e3a1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg><span style="color:#a6e3a1">활성</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div style="display:flex;align-items:center;gap:6px"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#f38ba8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/></svg><span style="color:#f38ba8">비활성</span></div>""", unsafe_allow_html=True)
        with col5:
            if st.button('보기', key=f"detail_{user['id']}"):
                st.session_state['selected_user'] = user
                st.rerun()

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button('선택 활성화', use_container_width=True, type='primary'):
            if not selected_ids:
                st.error('회원을 선택해주세요')
            else:
                for user in st.session_state['users']:
                    if user['id'] in selected_ids:
                        user['is_active'] = True
                st.success(f'{len(selected_ids)}명 활성화 완료')
                st.rerun()
    with col2:
        if st.button('선택 비활성화', use_container_width=True):
            if not selected_ids:
                st.error('회원을 선택해주세요')
            else:
                for user in st.session_state['users']:
                    if user['id'] in selected_ids:
                        user['is_active'] = False
                st.success(f'{len(selected_ids)}명 비활성화 완료')
                st.rerun()
