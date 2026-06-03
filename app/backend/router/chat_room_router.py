from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.model.chat_room import ChatRoom
from app.backend.schema.base_schema import PaginationRequest
from app.backend.schema.chat_room_schema import (
    ChatRoomPageResponse,
    ChatRoomCreateRequest,
    ChatRoomResponse,
    ChatRoomUpdateRequest,
)
from app.backend.service.chat_room_service import (
    delete_chat_room_service,
    get_all_chat_room_service,
    get_chat_room_service,
    patch_chat_room_service,
    post_chat_room_service,
)

router = APIRouter(
    prefix="/chat-rooms",
    tags=["chat-rooms"],
)

@router.post("",
             response_model=ChatRoomResponse,
             status_code=status.HTTP_201_CREATED,
             summary="채팅방 생성",
             description="채팅방을 생성합니다."
             )
def create_chat_room(request: ChatRoomCreateRequest, db: Session = Depends(get_db)):
    """
    채팅방 생성 API
    :param request: 채팅방 생성 요청 데이터
    :param db: 세션
    :return: 생성된 채팅방
    """
    return post_chat_room_service(db, request.member_id, request.title, request.persona)

@router.get("",
            response_model=ChatRoomPageResponse,
            summary="채팅방 목록 조회",
            description="채팅방 목록을 조회 합니다."
            )
def get_all_chat_rooms(
    pagination: PaginationRequest = Depends(),
    db: Session = Depends(get_db)
):
    """
    채팅방 목록 조회 API
    :param pagination: 페이징 정보
    :param db: 세션
    :return: 채팅방 목록
    """
    return get_all_chat_room_service(db, pagination)

@router.get("/{room_id}",
            response_model=ChatRoomResponse,
            summary="채팅방 조회",
            description="대화한 채팅방을 조회 합니다."
            )
def get_one_chat_room(room_id: int, db: Session = Depends(get_db)):
    """
    채팅방 단건 조회 API
    :param room_id: 대화방 PK
    :param db: 세션
    :return: 조회된 채팅방
    """
    return get_chat_room_service(db, room_id)

@router.patch("/{room_id}",
              response_model=ChatRoomResponse,
              summary="채팅방 수정",
              description="대화한 채팅방을 수정합니다."
              )
def update_chat_room(room_id: int, request: ChatRoomUpdateRequest, db: Session = Depends(get_db)):
    """
    채팅방 수정 API
    :param room_id: 대화방 PK
    :param request: 채팅방 수정 요청 데이터
    :param db: 세션
    :return: 수정된 채팅방
    """
    chat_room = ChatRoom(title=request.title, persona=request.persona)
    return patch_chat_room_service(db, room_id, chat_room)

@router.delete("/{room_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="채팅방 삭제",
               description="단건 채팅방을 삭제 합니다."
               )
def delete_chat_room(room_id: int, db: Session = Depends(get_db)):
    """
    채팅방 삭제 API
    :param room_id: 대화방 PK
    :param db: 세션
    :return: 없음
    """
    delete_chat_room_service(db, room_id)