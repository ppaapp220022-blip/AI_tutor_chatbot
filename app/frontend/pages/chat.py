import streamlit as st

st.set_page_config(
    page_title='AI Tutor Chatbot',
    page_icon='🤖',
    layout='wide'
)

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }

    [data-testid="stSidebar"] { background-color: #1e1e2e; }
    [data-testid="stSidebar"] * { color: #cdd6f4 !important; }
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

    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 8px;
    }

    [data-testid="stFileUploader"] { background: transparent !important; }
    [data-testid="stFileUploader"] section {
        border: 2px dashed #45475a;
        border-radius: 12px;
        padding: 10px 16px;
        background-color: transparent !important;
        transition: 0.2s;
    }
    [data-testid="stFileUploader"] section:hover { border-color: #89b4fa; }
    [data-testid="stFileUploaderDropzoneInstructions"] div span { font-size: 13px; }
    [data-testid="stFileUploaderDropzoneInstructions"] div small { display: none; }
    </style>
""", unsafe_allow_html=True)

if 'access_token' not in st.session_state:
    st.switch_page('pages/login.py')

if 'chat_rooms' not in st.session_state:
    st.session_state['chat_rooms'] = []
if 'current_room' not in st.session_state:
    st.session_state['current_room'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

PERSONAS = ['일반 튜터', '수학 전문가', '영어 전문가', '과학 전문가', '역사 전문가']


@st.dialog('새 채팅방 만들기')
def create_room_modal():
    room_title = st.text_input('채팅방 이름', placeholder='채팅방 이름을 입력하세요')
    persona = st.selectbox('페르소나 선택', PERSONAS)
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('만들기', use_container_width=True, type='primary'):
            if not room_title:
                st.error('채팅방 이름을 입력해주세요')
            else:
                new_room = {
                    'id': len(st.session_state['chat_rooms']) + 1,
                    'title': room_title,
                    'persona': persona
                }
                st.session_state['chat_rooms'].append(new_room)
                st.session_state['current_room'] = new_room
                st.session_state['messages'] = []
                st.rerun()
    with col2:
        if st.button('취소', use_container_width=True):
            st.rerun()


@st.dialog('채팅방 나가기')
def leave_room_modal(room):
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f38ba8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            <strong>'{room['title']}'</strong> 채팅방을 나가시겠습니까?
        </div>
        <p style="color:#888; font-size:13px">채팅방을 나가면 목록에서 삭제됩니다</p>
    """, unsafe_allow_html=True)
    st.write('')
    col1, col2 = st.columns(2)
    with col1:
        if st.button('나가기', use_container_width=True, type='primary'):
            st.session_state['chat_rooms'].remove(room)
            if st.session_state['current_room'] and st.session_state['current_room']['id'] == room['id']:
                st.session_state['current_room'] = None
                st.session_state['messages'] = []
            st.rerun()
    with col2:
        if st.button('취소', use_container_width=True):
            st.rerun()


# 사이드바
with st.sidebar:
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:8px; padding:4px 0">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#cdd6f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/></svg>
            <span style="font-size:16px; font-weight:600; color:#cdd6f4">{st.session_state.get('login_id', '')}님</span>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("""
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#cdd6f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <span style="font-size:15px; font-weight:600; color:#cdd6f4">채팅방 목록</span>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state['chat_rooms']:
        st.caption('채팅방이 없습니다')
    else:
        for room in st.session_state['chat_rooms']:
            col1, col2 = st.columns([4, 1])
            with col1:
                is_selected = (st.session_state['current_room'] and
                               st.session_state['current_room']['id'] == room['id'])
                btn_label = f"✓ {room['title']}" if is_selected else f"  {room['title']}"
                if st.button(btn_label, key=f"room_{room['id']}", use_container_width=True):
                    st.session_state['current_room'] = room
                    st.session_state['messages'] = []
                    st.rerun()
            with col2:
                if st.button('×', key=f"leave_{room['id']}", help='채팅방 나가기'):
                    leave_room_modal(room)

    st.divider()

    if st.session_state.get('role') == 'ADMIN':
        if st.button('관리자 페이지', use_container_width=True):
            st.switch_page('pages/admin.py')
        st.write('')

    if st.button('로그아웃', use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page('pages/login.py')


# 메인
if st.session_state['current_room'] is None:
    if not st.session_state['chat_rooms']:
        st.markdown('<br>' * 3, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style="text-align:center; margin-bottom:16px">
                    <svg xmlns="http://www.w3.org/2000/svg" width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
                    <h2 style="margin-top:8px">AI Tutor Chatbot</h2>
                    <p style="color:#888">학습을 도와주는 AI 튜터입니다</p>
                </div>
            """, unsafe_allow_html=True)
            st.divider()
            st.info('채팅방이 없습니다. 새 채팅방을 만들어보세요!')
            st.write('')
            if st.button('+ 새 채팅방 만들기', use_container_width=True, type='primary'):
                create_room_modal()
    else:
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown("""
                <div style="display:flex; align-items:center; gap:10px">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
                    <h2 style="margin:0">AI Tutor Chatbot</h2>
                </div>
                <p style="color:#888; margin-top:4px">채팅방을 선택하세요</p>
            """, unsafe_allow_html=True)
        with col2:
            st.write('')
            st.write('')
            if st.button('+ 새 채팅방', help='새 채팅방 만들기', use_container_width=True):
                create_room_modal()

        st.divider()
        cols = st.columns(3)
        for i, room in enumerate(st.session_state['chat_rooms']):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"""
                        <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                            <strong>{room['title']}</strong>
                        </div>
                        <p style="color:#888; font-size:13px; margin:0">페르소나 : {room['persona']}</p>
                    """, unsafe_allow_html=True)
                    st.write('')
                    if st.button('입장하기', key=f"enter_{room['id']}", use_container_width=True, type='primary'):
                        st.session_state['current_room'] = room
                        st.session_state['messages'] = []
                        st.rerun()
else:
    room = st.session_state['current_room']

    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px">
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#89b4fa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                <h2 style="margin:0">{room['title']}</h2>
            </div>
            <p style="color:#888; margin-top:4px; margin-left:38px">페르소나 : {room['persona']}</p>
        """, unsafe_allow_html=True)
    with col2:
        st.write('')
        st.write('')
        if st.button('+ 새 채팅방', use_container_width=True):
            create_room_modal()

    st.divider()

    for message in st.session_state['messages']:
        with st.chat_message(message['role']):
            st.write(message['content'])
            if message.get('file'):
                st.markdown(f"""
                    <div style="display:flex; align-items:center; gap:6px; color:#888; font-size:13px; margin-top:4px">
                        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
                        {message['file']}
                    </div>
                """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        '파일 첨부 (클릭하거나 드래그하세요)',
        label_visibility='visible',
        key='file_upload',
    )

    if uploaded_file:
        st.toast(f'파일 업로드됨: {uploaded_file.name}')

    if prompt := st.chat_input('메시지를 입력하세요'):
        msg = {'role': 'user', 'content': prompt}
        if uploaded_file:
            msg['file'] = uploaded_file.name
        st.session_state['messages'].append(msg)
        with st.chat_message('user'):
            st.write(prompt)
        with st.chat_message('assistant'):
            st.write('백엔드 연동 예정')
        st.session_state['messages'].append({'role': 'assistant', 'content': '백엔드 연동 예정'})
        st.rerun()
