from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.schema.ai_chat_schema import AiChatResponse
from app.backend.service.ai_chat_service import handle_chat_request_service

router = APIRouter(
    prefix="/chat-rooms/{room_id}/AiChat",
    tags=["ai_chat"],
)

@router.post("",
             response_model=AiChatResponse,
             status_code=status.HTTP_200_OK,
             summary="AI 채팅 시작",
             description="AI 채팅 객체를 생성합니다."
             )
def chat_with_ai(
    room_id: int,
    message: str = Form(...),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    """
    AI 채팅 요청 API
    :param room_id: 대화방 PK
    :param message: 사용자 메시지
    :param file: 업로드 파일
    :param db: 세션
    :return: AI 응답 결과
    """
    return handle_chat_request_service(db, room_id, message, file)