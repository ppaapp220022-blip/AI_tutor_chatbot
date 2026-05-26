from pydantic import BaseModel
from app.backend.model.users import Role

# 요청 (password 있음)
class UserRequest(BaseModel):
    login_id: str
    password: str
    email: str

# 응답 (password 제외)
class UserResponse(BaseModel):
    id: int
    login_id: str
    email: str
    role: Role
    is_active: bool

    class Config:
        from_attributes = True