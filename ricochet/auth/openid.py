from flask import json
from flask import url_for
from flask import g
from flask import session
from flask import request
from flask import redirect
from flask import Response

from openidredis import RedisStore
from flask.ext.openid import OpenID

from ricochet import app
from ricochet import models

# https://github.com/bbangert/openid-redis/issues/4
# pypi's version of openid-redis doesn't allow the conn
# argument, so for now we'll need to specify the args
# specifically, and we annoyingly can't define password.
store_factory = lambda: RedisStore(key_prefix='ricochet:oid',
                                   host=app.config['REDIS']['host'],
                                   port=app.config['REDIS']['port'],
                                   db=app.config['REDIS']['db'])
oid = OpenID(app, store_factory=store_factory)


@app.before_request
def before_request():
    g.user = None
    if 'identity_url' in session:
        g.user = models.User(session['identity_url'])

@app.route('/auth/login', methods = ['GET', 'POST'])
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

@app.route('/auth/logout', methods = ['GET', 'POST'])
def logout():
    if 'identity_url' in session:
        session.pop('identity_url')
    return json.dumps({})
