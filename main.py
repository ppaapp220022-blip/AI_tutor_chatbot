from fastapi import FastAPI

from app.backend.database import engine, Base
from app.backend.exception import register_exception_handlers
from app.backend.router.ai_chat_router import router as ai_chat_router
from app.backend.router.chat_room_router import router as chat_room_router
from app.backend.router.messages_router import router as messages_router
from app.backend.router.uploaded_files_router import router as uploaded_files_router
from loguru import logger
from dotenv import load_dotenv
import app.backend.model as backend_model
import sys

app = FastAPI()
register_exception_handlers(app)
app.include_router(ai_chat_router)
app.include_router(chat_room_router)
app.include_router(messages_router)
app.include_router(uploaded_files_router)

load_dotenv()

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 설정
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
def root():
    return {"message": "Hello World"}
