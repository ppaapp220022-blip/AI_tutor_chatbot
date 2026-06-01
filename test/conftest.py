import os
from pathlib import Path
from tempfile import gettempdir

import pytest
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = f"sqlite:///{Path(gettempdir()) / 'ai_tutor_chatbot_test.db'}"

from app.backend.database import Base, create_db_engine
from app.backend.service import uploaded_files_service

TEST_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_db_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def upload_dir(tmp_path, monkeypatch):
    test_upload_dir = tmp_path / "uploads"
    monkeypatch.setattr(uploaded_files_service, "UPLOAD_DIR", test_upload_dir)
    return test_upload_dir
