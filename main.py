from dotenv import load_dotenv
import sys

load_dotenv()

from fastapi import FastAPI
from loguru import logger

import app.backend.model
from app.backend.database import init_db

app = FastAPI()

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


@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Hello World"}
