import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.backend.database import Base

# 테스트용 DB
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ai_tutor_chatbot_test"
engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try :
        yield session # 테스트 세션 전달
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine) # 테스트 끝나면 테이블 삭제