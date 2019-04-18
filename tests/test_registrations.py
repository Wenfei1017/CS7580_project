import pytest
import json

sponsor_body = {
    'username': 'happyfive',
    'password': 'password',
    'email': 'happyfive@gmail.com',
    'role': 'Sponsor'
}

another_sponsor_body = {
    'username': 'happyfive2',
    'password': 'password',
    'email': 'happyfive@gmail.com',
    'role': 'Sponsor'
}

user_body = {
    'username': 'happyfiveuser',
    'password': 'password',
    'email': 'happyfiveuser@gmail.com',
    'role': 'User'
}

another_user_body = {
    'username': 'happyfiveuser2',
    'password': 'password',
    'email': 'happyfiveuser@gmail.com',
    'role': 'User'
}

event_body = {
    'title': 'Event101' ,
    'description': 'test',
    'time_start': '10/12/2020 16:21:42',
    'time_end': '10/12/2020 17:21:42',
    'event_address':'401 Terry Ave, 105',
    'category': 'others'
}

def test_create_registration_fail_anonymous(client, app):
    result = client.post('/registrations', json={'event_id': 1})
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in first'


def test_create_registration_fail_sponsor(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })

    result = client.post('/registrations', json={'event_id': 1})
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in as User first'

def test_create_registration_success(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=event_body)
    client.post('/users/logout')
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.post('/registrations', json={'event_id': 1})
    assert result.status_code == 201
    assert result.data.decode('utf8') == 'registered success'

    # test double registeration is not allowed
    result = client.post('/registrations', json={'event_id': 1})
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'already registered'
    

def test_get_registration_fail_anonymous(client, app):
    result = client.get('/registrations')
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in first'


def test_get_registration_fail_sponsor_no_event(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })

    result = client.get('/registrations', json={'event_id': 1})
    assert result.status_code == 403


def test_get_registration_fail_sponsor_invalid_sponsor(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=event_body)
    client.post('/users/logout')

    client.post('/users/register', json=another_sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive2',
        'password': 'password'
    })

    result = client.get('/registrations', json={'event_id': 1})
    assert result.status_code == 403


def test_get_registration_success_sponsor(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=event_body)
    client.post('/users/logout')
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })
    client.post('/registrations', json={'event_id': 1})
    client.post('/users/logout')
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })

    result = client.get('/registrations?event=1')
    assert result.status_code == 200

    result = client.get('/registrations?event=1&user=2')
    assert result.status_code == 200


def test_get_registration_success_user_all(client, app):
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.get('/registrations')

    assert result.status_code == 200

def test_get_registration_success_user_by_event_id(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=event_body)
    client.post('/users/logout')
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })
    client.post('/registrations', json={'event_id': 1})

    result = client.get('/registrations?event=1')
    assert result.status_code == 200


def test_get_registration_fail_invalid(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=event_body)
    client.post('/users/logout')
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })
    client.post('/registrations', json={'event_id': 1})
    
    result = client.get('registrations?user=2')
    assert result.status_code == 403
    
    client.post('/users/logout')
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    result = client.get('registrations?user=2')
    assert result.status_code == 403
    

def test_delete_registration_fail(client, app):
    result = client.delete('/registrations?event=1')
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in first'

def test_delete_registration_sponsor(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=event_body)
    client.post('/users/logout')
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })
    client.post('/registrations', json={'event_id': 1})
    client.post('/users/logout')
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })

    result = client.delete('/registrations', json={
        'event_id':1,
        'user_id': 2
        })
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in as User'


def test_delete_registration_user(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=event_body)
    client.post('/users/logout')
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })
    client.post('/registrations', json={"event_id":1})

    result = client.delete('/registrations?event=1')
    assert result.status_code == 204
    # assert result.data.decode('utf8') == 'Delete user registration success'