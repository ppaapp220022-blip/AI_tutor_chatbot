from pathlib import Path
from uuid import uuid4

from app.backend.repository.uploaded_files_repository import (
    create_uploaded_files,
    list_uploaded_files,
    find_uploaded_files,
    update_uploaded_files,
    delete_uploaded_files
)
from app.backend.repository.chat_room_repository import find_chat_room

UPLOAD_DIR = Path("uploads")


# 파일 업로드 저장소 생성
def post_uploaded_files_service(db, room_id: int, file_name: str, file_path: str, commit: bool = True):

    if not room_id:
        raise ValueError("채팅방을 확인 할 수 없습니다.")

    room = find_chat_room(db, room_id)
    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    uploaded = create_uploaded_files(db, room_id, file_name, file_path)

    if commit:
        db.commit()
        db.refresh(uploaded)

    return uploaded


def save_upload_file_service(db, room_id: int, upload_file, commit: bool = True):
    if not room_id:
        raise ValueError("채팅방을 확인할 수 없습니다.")

    room = find_chat_room(db, room_id)
    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    if not upload_file or not getattr(upload_file, "filename", None):
        raise ValueError("업로드 파일이 없습니다.")

    original_name = upload_file.filename
    if not original_name.lower().endswith(".pdf"):
        raise ValueError("pdf 파일만 업로드할 수 있습니다.")

    file_bytes = upload_file.file.read()
    if not file_bytes:
        raise ValueError("업로드 파일 내용이 비어 있습니다.")

    room_dir = UPLOAD_DIR / str(room_id)
    room_dir.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid4()}_{original_name}"
    stored_path = room_dir / stored_name

    try:
        with open(stored_path, "wb") as file_object:
            file_object.write(file_bytes)

        uploaded = post_uploaded_files_service(
            db,
            room_id=room_id,
            file_name=original_name,
            file_path=str(stored_path),
            commit=commit,
        )
        return uploaded
    except Exception:
        if stored_path.exists():
            stored_path.unlink()
        raise


# 파일 업로드 목록
def get_all_uploaded_files_service(db, room_id: int):
    room = find_chat_room(db, room_id)
    if not room:
        raise ValueError("채팅방이 존재하지 않습니다.")

    uploaded = list_uploaded_files(db, room_id)

    return uploaded

# 파일 업로드 단건 검색
def get_one_uploaded_files_service(db, uploaded_id: int):
    uploaded = find_uploaded_files(db, uploaded_id)

    if not uploaded:
        raise ValueError("업로드한 파일이 1건도 확인되지 않습니다.")

    return uploaded

# 파일 업로드 수정
def patch_uploaded_files_service(db, uploaded_id: int, new_file_name: str, new_file_path: str):
    uploaded = update_uploaded_files(db, uploaded_id, new_file_name, new_file_path)

    if not uploaded:
        raise ValueError("수정할 업로드 파일이 존재하지 않습니다.")

    db.commit()
    db.refresh(uploaded)
    return uploaded

# 파일 업로드 삭제
def delete_uploaded_files_service(db, uploaded_id: int):
    uploaded = find_uploaded_files(db, uploaded_id)

    if not uploaded:
        raise ValueError("삭제할 업로드 파일이 존재하지 않습니다.")

    delete_uploaded_files(db, uploaded_id)
    db.commit()
    return True
