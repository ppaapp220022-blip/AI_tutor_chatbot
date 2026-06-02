from pydantic import ConfigDict
from app.backend.model.users import Role
from app.backend.schema.base_schema import BaseSchema


# 요청 (password 있음)
class UserRequest(BaseSchema):
    login_id: str
    password: str
    email: str

    def __str__(self):
        # password 제외하고 출력
        return str(self.model_dump(exclude={'password'}))


# 응답 (password 제외)
class UserResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login_id: str
    email: str
    role: Role
    is_active: bool


# 단건 / 여러건 활성화 여부 변경
class UsersActiveRequest(BaseSchema):
    user_idx: list[int]
    is_active: bool
