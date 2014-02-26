ricochet
=======

A web interface for [Trebuchet](https://github.com/trebuchet-deploy/trebuchet).

Requirements
------------

* Flask>=0.8
* redis>=2.4.9

If OpenID authentication is needed:

* Flask-OpenID==1.1.1
* openid-redis==1.0
* python-openid==2.2.5

Ricochet isn't usable without trebuchet. It's a web interface that interacts
with trebuchet. It currently reads from the redis store that trebuchet writes
to.

Installation
------------

### Using pip ###

```bash
sudo pip install TrebuchetRicochet
```

Configuration
-------------

Configuration is handled via a flask configuration file, which can be defined
via the RICOCHET_SETTINGS environment variable. Here's the available
configuration and its defaults:

```python
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
    AUTH_BACKEND = 'openid',
    OPENID_FORCED_PROVIDER = 'https://www.google.com/accounts/o8/id',
    OPENID_PROVIDERS = {
        'google': 'https://www.google.com/accounts/o8/id'
    },
    DEPLOY_DIR = '/srv/deployment'
)
```

Usage
-----

Execute: runserver.py

After executing it, it'll be running on port 5000.

Demo
----

See a demo at: http://trebuchet.wmflabs.org (authentication support disabled
there).

Getting Help
------------

For bugs, please use the github issues tracker for this project. To discuss usage or development of ricochet, please join me on #trebuchet-deploy on Freenode.
