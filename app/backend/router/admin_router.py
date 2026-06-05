from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.backend.database import get_db
from app.backend.dependencies import get_current_users
from app.backend.schema.users_schema import (
    UsersActiveRequest,
    UserResponse,
    UserPageResponse,
    UserChatHistoryPageResponse,
)
from app.backend.service.user_service import (
    get_user_all,
    get_login_id,
    modify_active_user,
    get_user_chat_history,
)

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_current_users)]  # = Java - @RequestMapping()
)


@admin_router.get('/member',
                  response_model=UserPageResponse,
                  status_code=status.HTTP_200_OK,
                  summary='회원 목록 조회'
                  )
def get_members(
        db: Session = Depends(get_db),
        page: int = Query(default=1, ge=1, description='페이지 번호'),
        size: int = Query(default=10, ge=1, le=100, description='페이지 크기')
) -> UserPageResponse:
    """
    회원 전체 조회 (페이징)
    :param db: 세션
    :param page: 페이지 번호 (1부터 시작)
    :param size: 페이지 크기 (최대 100)
    :return: 페이징된 회원 목록
    """
    return get_user_all(db, page=page, size=size)


@admin_router.get('/member/{login_id}',
                  response_model=UserResponse,
                  status_code=status.HTTP_200_OK,
                  summary='회원 상세 조회'
                  )
def get_member(login_id: str, db: Session = Depends(get_db)) -> UserResponse:
    """
    회원 상세 조회
    :param login_id: 로그인 아이디
    :param db: 세션
    :return: 회원 상세 정보
    """
    return get_login_id(db, login_id)


@admin_router.get('/member/{login_id}/chat-history',
                  response_model=UserChatHistoryPageResponse,
                  status_code=status.HTTP_200_OK,
                  summary='회원 채팅 이력 조회'
                  )
def get_member_chat_history(
        login_id: str,
        db: Session = Depends(get_db),
        page: int = Query(default=1, ge=1, description='페이지 번호'),
        size: int = Query(default=10, ge=1, le=100, description='페이지 크기')
) -> UserChatHistoryPageResponse:
    """
    회원 채팅 이력 조회
    :param login_id: 로그인 아이디
    :param db: 세션
    :param page: 페이지 번호
    :param size: 페이지 크기
    :return: 채팅 이력 목록
    """
    return get_user_chat_history(db, login_id, page=page, size=size)


@admin_router.put('/member/activate',
                  status_code=status.HTTP_200_OK,
                  summary='회원 계정 활성화 여부 변경'
                  )
def activate_member(user: UsersActiveRequest, db: Session = Depends(get_db)) -> dict:
    """
    회원 활성화 / 비활성화 (단건 / 다건)
    :param user: 변경할 회원 PK 목록 및 활성화 여부
    :param db: 세션
    :return: 변경된 회원 수
    """
    count = modify_active_user(db, user)
    return {'message': f'{count}명 상태 변경 완료'}
