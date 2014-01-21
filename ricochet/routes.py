from functools import wraps
from flask import make_response
from flask import json
from flask import url_for
from flask import g
from flask import session
from flask import request
from flask import redirect
from flask import Response

from ricochet import app
from ricochet import models
from ricochet import oid


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

@app.route('/')
def index():
    return make_response(open('ricochet/templates/index.html').read())

@app.route('/repolist')
@check_auth
def repolist():
    repos = models.RepoList()

    return json.dumps(repos.get_list())

@app.route('/repo/<path:repo_name>')
@check_auth
def repo(repo_name):
    repo = models.Repo(repo_name)

    return repo.get_json()

@app.before_request
def before_request():
    g.user = None
    if 'identity_url' in session:
        g.user = models.User(session['identity_url'])

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(url_for('index'))
    openid = app.config['OPENID_FORCED_PROVIDER']
    return oid.try_login(openid, ask_for=['fullname',
                                          'image',
                                          'nickname',
                                          'email'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        return redirect(url_for('index'))
    user = models.User(resp.identity_url)
    if not user.exists():
        user.save(resp)
    session['identity_url'] = resp.identity_url
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if 'identity_url' in session:
        session.pop('identity_url')
    return json.dumps({})

@app.route('/user')
@check_auth
def user_info():
    if g.user is not None:
        return g.user.get_json()
    else:
        return json.dumps({})
