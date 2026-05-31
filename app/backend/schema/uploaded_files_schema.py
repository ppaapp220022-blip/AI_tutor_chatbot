from datetime import datetime

from pydantic import BaseModel

# 요청
class UploadedFileRequest(BaseModel):
    room_id: int
    file_name: str
    file_path: str

# 응답
class UploadedFileResponse(BaseModel):
    id: int
    room_id: int
    file_name: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True
