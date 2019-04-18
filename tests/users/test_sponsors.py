import pytest
import json

#dummy test for sponsor
def test_getSponsors(client, app):
    result = client.get('/sponsors')
    assert result.status_code == 500

def test_sponsor_events(client, app):
    result = client.get('/sponsor/happyfive')
    assert result.status_code == 500