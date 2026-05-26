from app.backend.repository.user_repository import create_users, find_user, update_user, delete_user


def test_create_users(db):
    login_id = 'user'
    password = '1234'
    email = 'user@example.com'

    user = create_users(db, login_id, password, email)

    assert user.id is not None
    assert user.login_id == 'user'
    assert user.password == '1234'
    assert user.email == 'user@example.com'

def test_find_users(db):
    login_id = 'user'
    password = '1234'
    email = 'user@example.com'
    create_users(db, login_id, password, email)

    login_id = 'user'
    find_user(db, login_id)

def test_update_user(db):
    login_id = 'user'
    password = '1234'
    email = 'user@example.com'
    create_users(db, login_id, password, email)
    new_password = '1111'
    new_email = 'user@naver.com'
    update_user(db, login_id, new_password, new_email)

def test_delete_user(db):
    login_id = 'user'
    password = '1234'
    email = ''
    create_users(db, login_id, password, email)
    delete_user(db, login_id)