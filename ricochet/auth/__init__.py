from functools import wraps
from flask import g
from flask import json
from flask import Response

from ricochet import app

if app.config['AUTH_BACKEND'] == 'openid':
    import ricochet.auth.openid


def authenticate():
    return Response('Not authenticated', 401)

def check_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if app.config['REQUIRE_AUTH']:
            if g.user is None:
                return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/user')
@check_auth
def user_info():
    if g.user is not None:
        return g.user.get_json()
    else:
        return json.dumps({})

@app.route('/auth/info')
@check_auth
def auth_info():
    if app.config['REQUIRE_AUTH']:
        return json.dumps({'auth_required': True})
    else:
        return json.dumps({'auth_required': False})
