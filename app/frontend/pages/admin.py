import streamlit as st
from typing import Any

from app.frontend.api.admin_api import fetch_member, fetch_member_chat_history, fetch_members, set_member_active
from app.frontend.api.auth_api import logout_user
from app.frontend.api.http_client import FrontendApiError

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

# 비로그인 사용자는 로그인 페이지 이동
if 'access_token' not in st.session_state:
    st.switch_page('pages/login.py')

# 관리자 권한이 아니면 채팅 페이지 이동
if st.session_state.get('role') != 'ADMIN':
    st.switch_page('pages/chat.py')

# 관리자 화면 기본 상태
if 'users' not in st.session_state:
    st.session_state['users'] = []
if 'selected_user' not in st.session_state:
    st.session_state['selected_user'] = None
if 'admin_page' not in st.session_state:
    st.session_state['admin_page'] = 1
if 'admin_page_size' not in st.session_state:
    st.session_state['admin_page_size'] = 10
if 'admin_total' not in st.session_state:
    st.session_state['admin_total'] = 0
if 'admin_total_pages' not in st.session_state:
    st.session_state['admin_total_pages'] = 1
if 'history_page' not in st.session_state:
    st.session_state['history_page'] = 1
if 'history_page_size' not in st.session_state:
    st.session_state['history_page_size'] = 5
if 'history_total' not in st.session_state:
    st.session_state['history_total'] = 0
if 'history_total_pages' not in st.session_state:
    st.session_state['history_total_pages'] = 1

try:
    # 회원 목록 조회
    member_payload = fetch_members(
        page=st.session_state['admin_page'],
        size=st.session_state['admin_page_size'],
    )
    st.session_state['users'] = member_payload.get('users', [])
    st.session_state['admin_total'] = member_payload.get('total', 0)
    st.session_state['admin_total_pages'] = member_payload.get('total_pages', 1)
except FrontendApiError as exc:
    st.error(exc.message)
    st.stop()

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
        # 서버와 세션 로그아웃 처리
        try:
            logout_user()
        except FrontendApiError:
            pass
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page('pages/login.py')

# 회원 상세 조회
if st.session_state['selected_user'] is not None:
    # 선택 회원 상세 조회
    selected_login_id = st.session_state['selected_user']['login_id']
    try:
        user = fetch_member(selected_login_id)
    except FrontendApiError as exc:
        st.error(exc.message)
        st.stop()

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
    try:
        history_payload = fetch_member_chat_history(
            selected_login_id,
            page=st.session_state['history_page'],
            size=st.session_state['history_page_size'],
        )
        history_items = history_payload.get('items', [])
        st.session_state['history_total'] = history_payload.get('total', 0)
        st.session_state['history_total_pages'] = history_payload.get('total_pages', 1)
    except FrontendApiError as exc:
        st.error(exc.message)
        history_items = []

    st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <strong>채팅 이력</strong>
        </div>
    """, unsafe_allow_html=True)

    if not history_items:
        st.info('채팅 이력이 없습니다')
    else:
        grouped_rooms: dict[tuple[int, str, str], list[dict[str, Any]]] = {}
        for item in history_items:
            room_key = (item['room_id'], item.get('title') or '제목 없는 채팅방', item.get('persona') or '일반 튜터')
            grouped_rooms.setdefault(room_key, []).append(item)

        for (room_id, title, persona), messages in grouped_rooms.items():
            with st.expander(f'방 #{room_id} - {title}'):
                st.caption(f'페르소나: {persona}')
                for message in messages:
                    role_label = '사용자' if str(message.get('role', '')).lower() == 'user' else 'AI'
                    st.markdown(
                        f"""
                        <div style="padding:10px 12px; border:1px solid #313244; border-radius:10px; margin-bottom:8px">
                            <div style="font-size:12px; color:#89b4fa; margin-bottom:4px">{role_label} / {message['created_at']}</div>
                            <div>{message['content']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    st.write("")
    hist_prev, hist_mid, hist_next = st.columns([1, 2, 1])
    with hist_prev:
        # 이전 이력 페이지 이동
        if st.button('이전 이력', use_container_width=True, disabled=st.session_state['history_page'] <= 1):
            st.session_state['history_page'] -= 1
            st.rerun()
    with hist_mid:
        st.markdown(
            f"<div style='text-align:center; padding-top:0.4rem'>"
            f"이력 페이지 {st.session_state['history_page']} / {st.session_state['history_total_pages']}"
            f"</div>",
            unsafe_allow_html=True,
        )
    with hist_next:
        # 다음 이력 페이지 이동
        if st.button(
            '다음 이력',
            use_container_width=True,
            disabled=st.session_state['history_page'] >= st.session_state['history_total_pages'],
        ):
            st.session_state['history_page'] += 1
            st.rerun()

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

    # 헤더 - E701 수정
    col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 1])
    with col1:
        st.write('**선택**')
    with col2:
        st.write('**아이디**')
    with col3:
        st.write('**이메일**')
    with col4:
        st.write('**상태**')
    with col5:
        st.write('**상세**')
    st.divider()

    for user in st.session_state['users']:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 1])
        with col1:
            checked = st.checkbox(' ', key=f"check_{user['id']}")
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
                st.session_state['history_page'] = 1
                st.rerun()

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        # 회원 활성화
        if st.button('선택 활성화', use_container_width=True, type='primary'):
            if not selected_ids:
                st.error('회원을 선택해주세요')
            else:
                try:
                    set_member_active(selected_ids, True)
                except FrontendApiError as exc:
                    st.error(exc.message)
                else:
                    st.success(f'{len(selected_ids)}명 활성화 완료')
                    st.rerun()
    with col2:
        # 회원 비활성화
        if st.button('선택 비활성화', use_container_width=True):
            if not selected_ids:
                st.error('회원을 선택해주세요')
            else:
                try:
                    set_member_active(selected_ids, False)
                except FrontendApiError as exc:
                    st.error(exc.message)
                else:
                    st.success(f'{len(selected_ids)}명 비활성화 완료')
                    st.rerun()

    st.write("")
    nav_prev, nav_mid, nav_next = st.columns([1, 2, 1])
    with nav_prev:
        # 이전 페이지 이동
        if st.button('이전 페이지', use_container_width=True, disabled=st.session_state['admin_page'] <= 1):
            st.session_state['admin_page'] -= 1
            st.rerun()
    with nav_mid:
        st.markdown(
            f"<div style='text-align:center; padding-top:0.4rem'>"
            f"페이지 {st.session_state['admin_page']} / {st.session_state['admin_total_pages']}"
            f"</div>",
            unsafe_allow_html=True,
        )
    with nav_next:
        # 다음 페이지 이동
        if st.button(
            '다음 페이지',
            use_container_width=True,
            disabled=st.session_state['admin_page'] >= st.session_state['admin_total_pages'],
        ):
            st.session_state['admin_page'] += 1
            st.rerun()
