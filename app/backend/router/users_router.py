from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.backend.database import get_db
from app.backend.dependencies import get_current_users
from app.backend.schema.users_schema import (
    UserRequest, UserResponse, LoginRequest, LoginResponse,
    OtpRequest, OtpVerifyRequest
)
from app.backend.service.user_service import (send_otp_code, vacillation_otp, add_user, modify_user)
from app.backend.service.jwt_login_service import login, logout

public_router = APIRouter(prefix='/users', tags=['users'])  # = Java - @RequestMapping()
private_router = APIRouter(prefix='/users', tags=['users'], dependencies=[Depends(get_current_users)])  # = Java - @RequestMapping()


@public_router.post('/send-otp',
                    status_code=status.HTTP_200_OK,
                    summary='OTP 이메일 인증'
                    )
def send_email_otp(request: OtpRequest) -> dict:
    """
    OTP 메일 발송
    :param request: 이메일 요청
    :return: 발송여부
    """
    send_otp_code(request.email)
    return {'message': 'OTP코드가 발송 되었습니다'}


@public_router.post('/verify-otp',
                    status_code=status.HTTP_200_OK,
                    summary='OTP코드 검증'
                    )
def verify_otp(request: OtpVerifyRequest) -> dict:
    """
    OTP Code 검증
    :param request: 이메일 및 OTP 요청
    :return: 검증 여부
    """
    vacillation_otp(request.email, request.otp_code)
    return {'message': '인증 완료'}


@public_router.post('/signup',
                    response_model=UserResponse,
                    status_code=status.HTTP_201_CREATED,
                    summary='회원가입'
                    )
def signup(request: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    """
    회원 가입
    :param request: 요청 스키마
    :param db: 세션
    :return: 회원가입 정보
    """
    return add_user(db, request)


@public_router.post('/login',
                    response_model=LoginResponse,
                    status_code=status.HTTP_200_OK,
                    summary='로그인'
                    )
def login_user(request: LoginRequest, db: Session = Depends(get_db)) -> JSONResponse:
    """
    로그인
    :param request: 로그인 정보가 담긴 요청 스키마
    :param db: 세션
    :return: 액세스 토큰 및 리프레시 토큰 쿠키
    """
    result = login(db, request)

    response = JSONResponse(
        content={
            'access_token': result['access_token'],
            'token_type': 'bearer',
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=result['refresh_token'],
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return response

@private_router.post('/logout',
                    status_code=status.HTTP_204_NO_CONTENT,
                    summary='로그아웃'
                    )
def logout_user(login_id: str = Depends(get_current_users())):
    logout(login_id)


@private_router.put('/modify',
                    response_model=UserResponse,
                    status_code=status.HTTP_200_OK,
                    summary="회원 정보 수정"
                    )
def modify_user_info(user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    """
    회원 정보 업데이트
    :param user: 회원 정보 요청 스키마
    :param db: 세션
    :return: 수정후 회원 정보
    """
    return modify_user(db, user)
