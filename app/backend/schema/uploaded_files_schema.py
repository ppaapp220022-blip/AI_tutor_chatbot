from datetime import datetime

from pydantic import BaseModel
from app.backend.schema.base_schema import PaginationResponse

# 파일 업로드 수정 스키마
class UploadedFileUpdateRequest(BaseModel):
    file_name: str | None = None
    file_path: str | None = None

# 파일 업로드 응답 스키마
class UploadedFileResponse(BaseModel):
    id: int
    room_id: int
    file_name: str
    file_path: str
    created_at: datetime

# 파일 업로드 설정 스키마
    class Config: # ModelMapper (SqlAlchemy -> Pydantic)
        from_attributes = True

class UploadedFilePageResponse(PaginationResponse):
    items: list[UploadedFileResponse]