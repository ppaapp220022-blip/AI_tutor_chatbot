from datetime import datetime, timezone, timedelta
import enum
from sqlalchemy import String, Boolean, Enum, DateTime, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.backend.database import Base

# UTC 기준 한국시간으로 지정
KST = timezone(timedelta(hours=9))


class Role(enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': '유저'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # PK
    login_id: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, comment='로그인 아이디')
    password: Mapped[str] = mapped_column(String(60), nullable=False, comment='비밀번호')
    email: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, comment='이메일')
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.USER, comment='유저 or 관리자')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment='계정 활성화 여부')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(KST), comment='생성일시')

    # FK (부모)
    chat_room = relationship('ChatRoom', back_populates='users')

    def __str__(self) -> str:
        # password 제외하고 출력
        return (f'Users(id={self.id}, login_id={self.login_id}, '
                f'email={self.email}, role={self.role}, '
                f'is_active={self.is_active}, created_at={self.created_at})')
