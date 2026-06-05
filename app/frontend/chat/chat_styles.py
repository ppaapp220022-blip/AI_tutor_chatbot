import streamlit as st


# 채팅 화면 전체에서 공통으로 쓰는 Streamlit 커스텀 스타일
CHAT_PAGE_STYLES = """
<style>
[data-testid="stSidebarNav"] { display: none; }

[data-testid="stSidebar"] { background-color: #1e1e2e; }
[data-testid="stSidebar"] * { color: #cdd6f4; }
[data-testid="stSidebar"] .stButton > button {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 8px;
    width: 100%;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #45475a;
    border-color: #585b70;
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

[data-testid="stFileUploader"] { background: transparent; }
[data-testid="stFileUploader"] section {
    border: 2px dashed #45475a;
    border-radius: 12px;
    padding: 10px 16px;
    background-color: transparent;
    transition: 0.2s;
}
[data-testid="stFileUploader"] section:hover { border-color: #89b4fa; }
[data-testid="stFileUploaderDropzoneInstructions"] div span { font-size: 13px; }
[data-testid="stFileUploaderDropzoneInstructions"] div small { display: none; }

.pager-label {
    text-align: center;
    font-size: 13px;
    color: #667085;
    margin-top: 4px;
    margin-bottom: 4px;
}
.sidebar-pager {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #313244;
}
[data-testid="stSidebar"] .sidebar-pager .stButton > button {
    border-radius: 999px;
    border: 1px solid #45475a;
    background: #2b2d42;
    color: #cdd6f4;
    font-weight: 600;
    min-height: 34px;
    padding: 0 10px;
}
[data-testid="stSidebar"] .sidebar-pager .stButton > button:hover {
    border-color: #89b4fa;
    background: #3a3d5a;
    transform: none;
    opacity: 1;
}
.lobby-page-info {
    margin-top: 14px;
    text-align: center;
    font-size: 13px;
    color: #667085;
}

.st-key-chat-composer {
    position: sticky;
    bottom: 0.75rem;
    z-index: 20;
    padding-top: 12px;
    background: linear-gradient(180deg, rgba(250,251,255,0) 0%, rgba(250,251,255,0.9) 18%, rgba(250,251,255,1) 35%);
}
.st-key-chat-composer form {
    padding: 10px 12px;
    border: 1px solid #d8def0;
    border-radius: 18px;
    background: #ffffff;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}
.st-key-chat-composer [data-testid="stHorizontalBlock"] {
    align-items: center;
}
.st-key-chat-composer [data-testid="column"] {
    display: flex;
    align-items: center;
}
.st-key-chat-composer [data-testid="column"] > div {
    width: 100%;
    margin-top: 0;
    margin-bottom: 0;
}
.st-key-chat-composer [data-testid="stFileUploader"] {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    margin-top: 0;
    margin-bottom: 0;
}
.st-key-chat-composer [data-testid="stFileUploader"] section {
    min-height: 40px;
    width: 100%;
    min-width: 0;
    max-width: 100%;
    padding: 0;
    border: none;
    border-radius: 12px;
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: stretch;
    box-shadow: none;
}
.st-key-chat-composer [data-testid="stFileUploader"] button {
    min-height: 40px;
    width: 100%;
    min-width: 0;
    border-radius: 12px;
    border: 1px solid #d8def0;
    background: #ffffff;
    color: #344054;
    font-weight: 600;
    padding: 0 14px;
    justify-content: center;
    box-sizing: border-box;
    white-space: nowrap;
}
.st-key-chat-composer [data-testid="stFileUploader"] button:hover {
    border-color: #89b4fa;
    background: #eef4ff;
}
.st-key-chat-composer [data-testid="stFileUploaderDropzoneInstructions"] {
    display: none;
}
.st-key-chat-composer [data-testid="stFileUploaderFile"] {
    display: none !important;
}
.st-key-chat-composer [data-testid="stFileUploaderFileData"] {
    display: none !important;
}
.st-key-chat-composer [data-testid="stFileUploaderFileName"] {
    display: none !important;
}
.st-key-chat-composer [data-testid="stFileUploaderDeleteBtn"] {
    display: none !important;
}
.st-key-chat-composer [data-testid="stFileUploaderFileList"] {
    display: none !important;
}
.st-key-chat-composer [data-testid="stFileUploader"] small,
.st-key-chat-composer [data-testid="stFileUploader"] ul,
.st-key-chat-composer [data-testid="stFileUploader"] li,
.st-key-chat-composer [data-testid="stFileUploader"] svg:not(button svg) {
    display: none !important;
}
.st-key-chat-composer [data-testid="stFileUploader"] p {
    margin: 0;
    padding: 0;
}
.st-key-chat-composer [data-testid="stBaseButton-secondary"] {
    width: 100%;
    min-width: 0;
    height: 40px;
    padding: 0 14px;
}
.st-key-chat-composer [data-testid="stTextInput"] {
    margin-top: 0;
    margin-bottom: 0;
}
.st-key-chat-composer [data-testid="stTextInputRootElement"] input {
    height: 40px;
    min-height: 40px;
    line-height: 40px;
    border-radius: 12px;
    border: 1px solid #d8def0;
    padding-top: 0;
    padding-bottom: 0;
    padding-left: 14px;
    padding-right: 14px;
    background: #ffffff;
    box-sizing: border-box;
}
.st-key-chat-composer [data-testid="stFormSubmitButton"] {
    margin-top: 0;
    margin-bottom: 0;
}
.st-key-chat-composer [data-testid="stFormSubmitButton"] button {
    min-height: 40px;
    border-radius: 12px;
    font-weight: 600;
    background: linear-gradient(135deg, #4f7cff 0%, #6da8ff 100%);
    border: 1px solid #4f7cff;
    color: #ffffff;
    padding: 0 14px;
}
.st-key-chat-composer [data-testid="stFormSubmitButton"] button:hover {
    border-color: #4f7cff;
    background: linear-gradient(135deg, #4773ee 0%, #629fff 100%);
    transform: none;
    filter: none;
}
.composer-file-name {
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border: 1px solid #d8def0;
    border-radius: 12px;
    background: #f8faff;
    font-size: 12px;
    color: #667085;
    text-align: left;
}
.composer-file-label {
    flex: 0 0 auto;
    font-weight: 700;
    color: #475467;
}
.composer-file-value {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
</style>
"""

def apply_chat_styles() -> None:
    # 채팅 페이지 진입 시 한 번만 전역 스타일을 주입한다.
    """Apply the page-wide CSS used by the chat experience."""
    st.markdown(CHAT_PAGE_STYLES, unsafe_allow_html=True)
