import subprocess

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.backend.database import engine, Base
from loguru import logger
from dotenv import load_dotenv
import app.backend.model as backend_model
import sys


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
