import subprocess
import sys
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from app.backend.database import engine, Base
from app.backend.router.users_router import public_router, private_router
from app.backend.router.admin_router import admin_router
import app.backend.model as backend_model

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

# router 등록
app.include_router(public_router)
app.include_router(private_router)
app.include_router(admin_router)

# 전역 예외 핸들러
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)}
    )

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
