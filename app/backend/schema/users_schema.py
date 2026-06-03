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


# 로그인 요청
class LoginRequest(BaseSchema):
    login_id: str
    password: str

    def __str__(self):
        # password 제외하고 출력
        return str(self.model_dump(exclude={'password'}))


# OTP 발송 요청
class OtpRequest(BaseSchema):
    email: str


# OTP 검증 요청
class OtpVerifyRequest(BaseSchema):
    email: str
    otp_code: str


# 응답 (password 제외)
class UserResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login_id: str
    email: str
    role: Role
    is_active: bool


# 페이징 응답
class UserPageResponse(BaseSchema):
    users: list[UserResponse]
    total: int
    page: int
    size: int
    total_pages: int


# 로그인 응답
class LoginResponse(BaseSchema):
    access_token: str
    token_type: str


# 단건 / 여러건 활성화 여부 변경
class UsersActiveRequest(BaseSchema):
    user_idx: list[int]
    is_active: bool
