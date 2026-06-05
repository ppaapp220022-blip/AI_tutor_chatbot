from app.backend.exception import register_exception_handlers
from app.backend.router.ai_chat_router import router as ai_chat_router
from app.backend.router.chat_room_router import router as chat_room_router
from app.backend.router.messages_router import router as messages_router
from app.backend.router.uploaded_files_router import router as uploaded_files_router
import subprocess
import sys
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.backend.database import engine, Base
from app.backend.router.users_router import public_router, private_router
from app.backend.router.admin_router import admin_router
import app.backend.model as _model  # noqa: F401 - Base.metadata.create_all() 모델 인식용

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # streamlit 같이 실행
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "app/frontend/main.py",
        "--server.port=8501"
    ])
    yield


app = FastAPI(lifespan=lifespan)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit 주소
    allow_credentials=True,  # 쿠키 허용
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 예외 핸들러
register_exception_handlers(app)

# router 등록
app.include_router(public_router)
app.include_router(private_router)
app.include_router(admin_router)
app.include_router(ai_chat_router)
app.include_router(chat_room_router)
app.include_router(messages_router)
app.include_router(uploaded_files_router)

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 로그 설정
logger.remove()  # 기본 설정 제거
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    "logs/app.log",       # 파일로도 저장
    rotation="1 day",     # 하루마다 새 파일
    retention="30 days",  # 30일치 보관
    level="DEBUG"
)


@app.get("/")
def root() -> dict:
    return {"message": "Hello World"}
