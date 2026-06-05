import pytest
from app.backend.model.users import Users, Role
from app.backend.repository.user_repository import create_users
from app.backend.schema.users_schema import LoginRequest
from app.backend.service.jwt_login_service import login
from app.backend.service.user_service import pwd_encoding


# 헬퍼 함수
def make_user(db, login_id: str = 'test', password: str = 'password123', email: str = 'test@test.com') -> Users:
    hashed_password = pwd_encoding.hash(password)
    user = Users(login_id=login_id, password=hashed_password, email=email, role=Role.USER)
    return create_users(db, user)


def make_login_request(login_id: str = 'test', password: str = 'password123') -> LoginRequest:
    return LoginRequest(login_id=login_id, password=password)


# 로그인 테스트
def test_login_success(db):
    # given
    make_user(db)
    request = make_login_request()

    # when
    result = login(db, request)

    # then
    assert result is not None
    assert 'access_token' in result
    assert 'refresh_token' in result
    assert result['token_type'] == 'bearer'


def test_login_not_found(db):
    # given
    request = make_login_request('없는유저')

    # when & then
    with pytest.raises(ValueError, match='아이디 또는 비밀번호가 틀렸습니다.'):
        login(db, request)


def test_login_wrong_password(db):
    # given
    make_user(db)
    request = make_login_request(password='wrong_password')

    # when & then
    with pytest.raises(ValueError, match='아이디 또는 비밀번호가 틀렸습니다.'):
        login(db, request)


def test_login_inactive_user(db):
    # given
    user = make_user(db)
    user.is_active = False
    db.commit()
    request = make_login_request()

    # when & then
    with pytest.raises(ValueError, match='비활성화 된 아이디 입니다.'):
        login(db, request)
