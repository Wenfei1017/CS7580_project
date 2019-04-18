import pytest
import json
from eventmanager.events.model import Event
from eventmanager.events.controller import define_event_status
from datetime import datetime

sponsor_body = {
    'username': 'happyfive',
    'password': 'password',
    'email': 'happyfive@gmail.com',
    'role': 'Sponsor'
}

invalid_sponsor_body = {
    'username': 'happyfive_test',
    'password': 'password',
    'email': 'happyfive_test@gmail.com',
    'role': 'Sponsor'
}

user_body = {
    'username': 'happyfiveuser',
    'password': 'password',
    'email': 'happyfiveuser@gmail.com',
    'role': 'User'
}

correct_event_body = {
    'title': 'Event101',
    'description': 'test',
    'time_start': '10/12/2020 16:21:42',
    'time_end': '10/12/2020 17:21:42',
    'event_address': '401 Terry Ave, 105',
    'category': 'others'
}

incorrect_event_body = {
    'title': 'Event101',
    'description': 'test',
    'time_start': '10/12/2020 16:21:42',
    'time_end': '10/12/2020 17:21:42',
    'event_address': '401 Terry Ave, 105',
    'category': 'test'
}

updated_event_body = {
    'title': 'Event101',
    'description': 'updated',
    'time_start': '10/12/2020 16:21:42',
    'time_end': '10/12/2020 17:21:42',
    'event_address': '401 Terry Ave, 105',
    'category': 'others'
}

get_event_body = {
    'id': 1,
    'title': 'Event101',
    'description': 'this is an event about pets, people who love pets are welcomed',
    'time_start': 'May 3rd, 2pm',
    'time_end': 'May 3rd, 3pm',
    'event_address': '401 Terry Ave, 105',
    'category': 'others',
    'sponsor_id': 0,
    'status': 'starting soon'
}


def test_new_event_fail_anonymous(client, app):
    result = client.post('/events/new', json=correct_event_body)
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_new_event_fail_user(client, app):
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.post('/events/new', json=correct_event_body)
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_new_event_fail_wrong_category(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })

    result = client.post('/events/new', json=incorrect_event_body)
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'this category does not exist'


def test_new_event_success(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })

    result = client.post('/events/new', json=correct_event_body)
    assert result.status_code == 200
    assert result.data.decode('utf8') == 'event create successful'


def test_get_events_fail_anonymous(client, app):
    result = client.get('/events', json=get_event_body)
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_get_events_fail_user(client, app):
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.get('/events', json=get_event_body)
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_get_events_sucess(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })

    result = client.get('/events', json=get_event_body)
    assert result.status_code == 200


def test_get_event_get(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)
    result = client.get('/events/1')
    assert result.status_code == 200


def test_get_event_update_fail_anonymous(client, app):
    result = client.put('/events/1', json=updated_event_body)
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_get_event_update_fail_user(client, app):
    client.post('/users/register', json=user_body)
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.put('/events/1', json=updated_event_body)
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_get_event_update_fail_invalid_sponsor(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)
    client.post('/users/logout')

    client.post('/users/register', json=invalid_sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive_test',
        'password': 'password'
    })

    result = client.put('/events/1', json=updated_event_body)
    assert result.status_code == 405
    assert result.data.decode('utf8') == 'Unauthorized'


def test_get_event_update_success(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)
    result = client.put('/events/1', json=updated_event_body)
    assert result.status_code == 200
    assert result.data.decode('utf8') == 'update successfully'
    updated_event = Event.query.get_or_404(1)
    assert updated_event.description == 'updated'


def test_get_event_delete_fail_anonymous(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    result = client.post('/events/new', json=correct_event_body)
    client.post('/users/logout')
    result = client.put('/events/1', json=updated_event_body)
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_get_event_delete_fail_user(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)
    client.post('/users/logout')
    client.post('/users/login', json={
        'username': 'happyfiveuser',
        'password': 'password'
    })

    result = client.put('/events/1')
    assert result.status_code == 403
    assert result.data.decode('utf8') == 'Method not allowed'


def test_get_event_delete_fail_invalid_sponsor(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)
    client.post('/users/logout')

    client.post('/users/register', json=invalid_sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive_test',
        'password': 'password'
    })

    result = client.delete('/events/1')
    assert result.status_code == 403


def test_get_event_delete_success(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)

    result = client.delete('/events/1')
    assert result.status_code == 200
    assert result.data.decode('utf8') == 'delete successfully'


def test_get_all_event_by_status_fail_invalid_status(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)

    result = client.get('/events/status/test')
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'this status does not exist'


def test_get_all_event_by_status_success(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)

    result = client.get('/events/status/Starting_soon')
    assert result.status_code == 200


def test_get_all_event_in_category_fail_invalid_category(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)

    result = client.get('/events/test')
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'this category does not exist'


def test_get_all_event_in_category_success(client, app):
    client.post('/users/register', json=sponsor_body)
    client.post('/users/login', json={
        'username': 'happyfive',
        'password': 'password'
    })
    client.post('/events/new', json=correct_event_body)

    result = client.get('/events/others')
    assert result.status_code == 200


def test_sort_events_fail(client, app):
    result = client.get('/events/sort?sort_by=test')
    assert result.status_code == 400
    assert result.data.decode('utf8') == 'Order criteria is not supported'


def test_sort_events_success(client, app):
    result = client.get('/events/sort?sort_by=location')
    assert result.status_code == 200

    result = client.get('/events/sort?sort_by=time_start')
    assert result.status_code == 200


def test_search_events_by_time_start(client, app):
    result = client.get('/events/search?time_start=01/01/2011 20:05:20')
    assert result.status_code == 200


def test_search_events_by_time_end(client, app):
    result = client.get('/events/search?time_end=01/01/2011 20:05:20')
    assert result.status_code == 200


def test_search_events_by_location(client, app):
    result = client.get('/events/search?location=sea')
    assert result.status_code == 200


def test_search_events_by_time_and_location(client, app):
    result = client.get('events/search?time_end=01/01/2033 20:00:00&location=sea')
    assert result.status_code == 200


def test_define_event_status_starting_soon():
    event = Event()
    event.title = 'event_101'
    event.description ='updated'
    event.time_start = datetime(2020, 4, 10, 16, 4, 54, 985990)
    event.time_end = datetime(2020, 4, 11, 16, 4, 54, 985990)
    event.event_address = '401 Terry Ave, 105'
    event.category = 'others'

    define_event_status(event)
    assert  event.status == 'Starting_soon'


def test_define_event_status_finished():
    event = Event()
    event.title = 'event_101'
    event.description ='updated'
    event.time_start = datetime(2018, 4, 10, 16, 4, 54, 985990)
    event.time_end = datetime(2018, 4, 11, 16, 4, 54, 985990)
    event.event_address = '401 Terry Ave, 105'
    event.category = 'others'

    define_event_status(event)
    assert  event.status == 'Finished'


def test_define_event_status_opening_now():
    event = Event()
    event.title = 'event_101'
    event.description ='updated'
    event.time_start = datetime.now()
    event.time_end = datetime(2033, 4, 11, 16, 4, 54, 985990)
    event.event_address = '401 Terry Ave, 105'
    event.category = 'others'

    define_event_status(event)
    assert  event.status == 'Opening_now'