from datetime import datetime, timezone, timedelta
import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.backend.database import Base

# UTC 기준 한국시간으로 지정
KST = timezone(timedelta(hours=9))

class Role(enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': '유저'}

    id: int = Column(Integer, primary_key=True, autoincrement=True) # PK
    login_id: str = Column(String(30), unique=True, nullable=False, comment='로그인 아이디')
    password: str = Column(String(60), nullable=False, comment='비밀번호')
    email: str = Column(String(40), unique=True, nullable=False, comment='이메일')
    role: Role = Column(Enum(Role), nullable=False, default=Role.USER, comment='유저 or 관리자')
    is_active: bool = Column(Boolean, default=True, comment='계정 활성화 여부')
    created_at: datetime = Column(DateTime, default=lambda: datetime.now(KST), comment='생성일시')

    # FK (부모)
    chat_room = relationship('ChatRoom', back_populates='users')
