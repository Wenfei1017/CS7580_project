from eventmanager.sponsors.model import Sponsor
import json

def obj_to_rep(obj):
    return {
    'id': obj.id,
    'username': obj.username,
    'email': obj.email
    }

def get_all_sponsors():
    result = Sponsor.query.all()
    print(result)
    return json.dumps([obj_to_rep(r) for r in result])
