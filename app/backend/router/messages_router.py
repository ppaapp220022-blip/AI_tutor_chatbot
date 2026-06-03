from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.exception import NotFoundException
from app.backend.schema.base_schema import PaginationRequest
from app.backend.schema.messages_schema import (
    MessageCreateRequest,
    MessagePageResponse,
    MessageResponse,
    MessageUpdateRequest,
)
from app.backend.service.messages_service import (
    delete_messages_service,
    get_all_messages_service,
    get_one_messages_service,
    patch_messages_service,
    post_messages_service,
)

router = APIRouter(
    prefix="/chat-rooms/{room_id}/messages",
    tags=["messages"],
)

@router.post("",
             response_model=MessageResponse,
             status_code=status.HTTP_201_CREATED,
             summary="메시지 생성",
             description="대화 메시지 객체를 생성 합니다."
             )
def create_message(room_id: int, request: MessageCreateRequest, db: Session = Depends(get_db)):
    """
    메시지 생성 API
    :param room_id: 대화방 PK
    :param request: 메시지 생성 요청 데이터
    :param db: 세션
    :return: 생성된 메시지
    """
    return post_messages_service(db, room_id, request.role, request.content)

@router.get("",
            response_model=MessagePageResponse,
            summary="메시지 목록 조회",
            description="대화 메시지 목록을 조회 합니다.")
def get_all_messages(
    room_id: int,
    pagination: PaginationRequest = Depends(),
    db: Session = Depends(get_db)
):
    """
    메시지 목록 조회 API
    :param room_id: 대화방 PK
    :param pagination: 페이징 정보
    :param db: 세션
    :return: 메시지 목록
    """
    return get_all_messages_service(db, room_id, pagination)

@router.get("/{message_id}",
            response_model=MessageResponse,
            summary="메시지 조회",
            description="대화 메시지를 조회 합니다."
            )
def get_one_message(room_id: int, message_id: int, db: Session = Depends(get_db)):
    """
    메시지 단건 조회 API
    :param room_id: 대화방 PK
    :param message_id: 메시지 PK
    :param db: 세션
    :return: 조회된 메시지
    """
    message = get_one_messages_service(db, message_id)
    if message.room_id != room_id:
        raise NotFoundException("메시지가 해당 채팅방에 존재하지 않습니다.")
    return message

@router.patch("/{message_id}",
              response_model=MessageResponse,
              summary="메시지 수정",
              description="대화 메시지를 수정 합니다."
              )
def update_message(room_id: int, message_id: int, request: MessageUpdateRequest, db: Session = Depends(get_db)):
    """
    메시지 수정 API
    :param room_id: 대화방 PK
    :param message_id: 메시지 PK
    :param request: 메시지 수정 요청 데이터
    :param db: 세션
    :return: 수정된 메시지
    """
    message = get_one_messages_service(db, message_id)
    if message.room_id != room_id:
        raise NotFoundException("메시지가 해당 채팅방에 존재하지 않습니다.")
    return patch_messages_service(db, message_id, request.content)

@router.delete("/{message_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="메시지 삭제",
               description="대화 메시지를 삭제 합니다."
               )
def delete_message(room_id: int, message_id: int, db: Session = Depends(get_db)):
    """
    메시지 삭제 API
    :param room_id: 대화방 PK
    :param message_id: 메시지 PK
    :param db: 세션
    :return: 없음
    """
    message = get_one_messages_service(db, message_id)
    if message.room_id != room_id:
        raise NotFoundException("메시지가 해당 채팅방에 존재하지 않습니다.")
    delete_messages_service(db, message_id)