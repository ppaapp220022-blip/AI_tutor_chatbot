from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.database import Base

KST = timezone(timedelta(hours=9))

class UploadedFiles(Base):
    __tablename__ = 'uploaded_files'
    __table_args__ = {'comment' : '파일 업로드'}

    id: int = Column(Integer, primary_key=True, autoincrement=True, comment='파일 고유 번호')
    room_id: int = Column(Integer, ForeignKey("chat_rooms.id"),nullable=True, comment='대화방 FK') # FK
    file_name: str = Column(String(50), nullable=True, comment='파일명')
    file_path: str = Column(String(255), nullable=True, comment='파일 경로')
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(KST), comment='생성일')

    # FK (자식)
    chat_room = relationship('ChatRoom', back_populates='uploaded_files')