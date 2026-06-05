from datetime import datetime, timezone, timedelta
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.backend.database import Base

KST = timezone(timedelta(hours=9))


class ChatRoom(Base):
    __tablename__ = 'chat_rooms'
    __table_args__ = {'comment': '대화방'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, comment='회원')  # FK
    title: Mapped[str] = mapped_column(String(20), nullable=True, comment='대화방 제목')
    persona: Mapped[str] = mapped_column(String(50), nullable=True, comment='페르소나 종류')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(KST), comment='생성일시')

    # FK (부모)
    messages = relationship('Messages', back_populates='chat_room')
    uploaded_files = relationship('UploadedFiles', back_populates='chat_room')

    # FK (자식)
    users = relationship('Users', back_populates='chat_room')
