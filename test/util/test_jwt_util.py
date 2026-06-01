import pytest
from app.backend.util.jwt_util import create_access_token, create_refresh_token, decode_token


# 헬퍼 함수
def make_access_token(login_id: str = 'test') -> str:
    return create_access_token(login_id)


def make_refresh_token(login_id: str = 'test') -> str:
    return create_refresh_token(login_id)


# 액세스 토큰 테스트
def test_create_access_token():
    # given
    login_id = 'test'

    # when
    token = make_access_token(login_id)

    # then
    assert token is not None
    assert isinstance(token, str)


def test_decode_access_token():
    # given
    token = make_access_token('test')

    # when
    decoded_id = decode_token(token)

    # then
    assert decoded_id == 'test'


# 리프레시 토큰 테스트
def test_create_refresh_token():
    # given
    login_id = 'test'

    # when
    token = make_refresh_token(login_id)

    # then
    assert token is not None
    assert isinstance(token, str)


def test_decode_refresh_token():
    # given
    token = make_refresh_token('test')

    # when
    decoded_id = decode_token(token)

    # then
    assert decoded_id == 'test'


# 유효하지 않은 토큰 테스트
def test_decode_invalid_token():
    # when & then
    with pytest.raises(ValueError):
        decode_token('invalid_token')
