from flask import Flask
from flask.ext.openid import OpenID
from openid.server import server
from openidredis import RedisStore
from redis import Redis

app = Flask(__name__)
app.config.update(
    CSRF_ENABLED = True,
    DEBUG = True,
    SECRET_KEY = 'development key',
    REQUIRE_AUTH = False,
    BACKEND = 'redis',
    REDIS = {
        'host': 'localhost',
        'port': 6379,
        'password': None,
        'db': 0
    },
    OPENID_FORCED_PROVIDER = 'https://www.google.com/accounts/o8/id',
    OPENID_PROVIDERS = {
        'google': 'https://www.google.com/accounts/o8/id'
    },
    DEPLOY_DIR = '/srv/deployment'
)
app.config.from_envvar('RICOCHET_SETTINGS', silent=True)

# Needed for the models and will hopefully be usable for
# the factory below later.
redis = Redis(**app.config['REDIS'])

# https://github.com/bbangert/openid-redis/issues/4
# pypi's version of openid-redis doesn't allow the conn
# argument, so for now we'll need to specify the args
# specifically, and we annoyingly can't define password.
store_factory = lambda: RedisStore(key_prefix='ricochet:oid',
                                   host=app.config['REDIS']['host'],
                                   port=app.config['REDIS']['port'],
                                   db=app.config['REDIS']['db'])
oid = OpenID(app, store_factory=store_factory)

import ricochet.routes
