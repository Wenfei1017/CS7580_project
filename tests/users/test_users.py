import pytest
import json
from eventmanager import bcrypt
from eventmanager.users.model import User, RoleEnum

user_reg_body = {
    'username': 'happyfive',
    'password': 'password',
    'email': 'happyfive@gmail.com',
    'role': 'Sponsor'
}


def test_create_user_success(client, app):
    # test that successful registration
    result = client.post('/users/register', json=user_reg_body)
    assert result.status_code == 201
    assert result.data.decode('utf8') == 'register successful'

    # test that the user was inserted into the database
    with app.app_context():
        user = User.query.filter_by(username=user_reg_body['username']).first()
        assert user is not None
        assert user.username == 'happyfive'
        assert bcrypt.check_password_hash(user.password, 'password')
        assert user.email == 'happyfive@gmail.com'
        assert user.role == RoleEnum.Sponsor


def test_create_user_fail(client, app):
    # test that successful registration
    result = client.post('/users/register', json={
        'username': 'happyfive1',
        'password': 'password',
        'email': 'happyfive1@gmail.com',
        'role': 'Sponsor1'
    })
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'role is incorrect, register failed'


def test_login_success(client):
    client.post('/users/register', json=user_reg_body)
    result = client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    assert result.status_code == 200
    assert result.data.decode('utf8') == 'login successful'


def test_login_fail(client):
    client.post('/users/register', json=user_reg_body)
    result = client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'wrongpassword'
    })
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'login failed'


def test_logout(client):
    client.post('/users/register', json=user_reg_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    result = client.post('/users/logout')
    assert result.status_code == 200
    assert result.data.decode('utf8') == 'logout successful'


def test_get_account_success(client):
    client.post('/users/register', json=user_reg_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    result = client.get('/users/account')
    assert result.status_code == 200
    assert result.data.decode('utf8') == json.dumps({
        'id': 1,
        "username": "happyfive",
        "email": "happyfive@gmail.com",
        "role": "Sponsor"
    })


def test_get_account_fail(client):
    result = client.get('/users/account')
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in first'


def test_put_account(client,app):
    client.post('/users/register', json=user_reg_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    result = client.put('/users/account', json={
        'username': 'happyfive1',
        'password': 'password',
        'email': 'happyfive@gmail.com',
    })
    assert result.status_code == 200
    assert result.data.decode('utf8') == 'update user success'
    # test that the user was updated in the database
    with app.app_context():
        user = User.query.filter_by(username='happyfive1').first()
        assert user is not None
        assert user.username == 'happyfive1'
        assert bcrypt.check_password_hash(user.password, 'password')
        assert user.email == 'happyfive@gmail.com'
        assert user.role == RoleEnum.Sponsor
