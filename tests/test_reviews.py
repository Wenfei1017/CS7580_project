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

review_body = {
    'review_time': '11/22/2020 20:05:20',
    'review_rating': 5,
    'review_content':'Great event'
}

def test_get_all_reviews_success(client, app):
    result = client.get('/reviews/all')
    assert result.status_code == 200


def test_update_review_by_id_failed_anonymous(client, app):
    result = client.post('/events/1/users/1/review')
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in first'


def test_update_review_by_id_failed_invalid_user(client, app):
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

    result = client.post('/events/1/users/1/review', json=review_body)
    assert result.status_code == 403


def test_update_review_by_id_success(client, app):
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

    # result = client.post('/events/1/users/2/review', json=review_body)
    # assert result.status_code == 200
    result = client.put('/events/1/users/2/review', json=review_body)
    assert result.status_code == 200


def test_get_review_by_id_failed_not_found(client, app):
    result = client.get('/events/1/users/1/review"')
    assert result.status_code == 404


def test_get_review_by_id_failed_not_reviewed(client, app):
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

    result = client.get('/events/1/users/2/review')
    assert result.status_code == 404
    assert result.data.decode('utf8') == 'Not reviewed yet'


def test_get_review_by_id_success(client, app):
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
    client.put('/events/1/users/2/review', json=review_body)
    
    result = client.get('/events/1/users/2/review')
    assert result.status_code == 200


def test_delete_review_by_id_failed_anonymous(client, app):
    result = client.delete('/events/1/users/1/review')
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in first'


def test_delete_review_by_id_failed_invalid_user(client, app):
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
    client.put('/events/1/users/2/review', json=review_body)
    client.post('/users/logout')
    client.post('/users/register', json=another_user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser2',
        'password': 'password'
    })

    result = client.delete('/events/1/users/2/review')
    assert result.status_code == 403


def test_delete_review_by_id_success(client, app):
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
    client.put('/events/1/users/2/review', json=review_body)

    result = client.delete('/events/1/users/2/review')
    assert result.status_code == 200
    assert result.data.decode('utf8') == 'Delete review success'


# @reviews.route("/reviews", methods=['GET'])
def test_query_reviews_by_event_and_or_user_failed_anonymous(client, app):
    result = client.get('/reviews')
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Please log in first'

def test_query_reviews_by_event_and_or_user_failed_none(client, app):
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.get('/reviews')
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'query with at least one of user''s id or event''s id'


def test_query_reviews_by_event_and_or_user_failed_success(client, app):
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.get('/reviews?event=1&user=1')
    assert result.status_code == 200

    result = client.get('/reviews?event=1')
    assert result.status_code == 200

    result = client.get('/reviews?user=1')
    assert result.status_code == 200
