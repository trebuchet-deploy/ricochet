import redis
import time
import os

from ricochet import app
from ricochet import redis
from flask import json


class User(object):

    def __init__(self, identity_url):
        self.identity_url = identity_url
        self.key = 'ricochet:users:{0}'.format(identity_url)
        self._load_user()

    def _load_user(self):
        self.data = redis.hgetall(self.key)

    def get_name(self):
        return self.data['fullname']

    def exists(self):
        return 'identity_url' in self.data

    def save(self, openid):
        mapping = {
            'identity_url': openid.identity_url,
            'fullname': openid.fullname,
            'nickname': openid.nickname,
            'email': openid.email
        }
        redis.hmset(self.key, mapping)

    def get_json(self):
        return json.dumps(redis.hgetall(self.key))


class Repo(object):

    def __init__(self, repo_name):
        self.repo_name = repo_name;
        self.deploy_data = {}
        self.minion_data = {}
        self.lock_data = {}
        repo_list = RepoList()
        if repo_name in repo_list.get_list():
            self._load_data()

    def _load_data(self):
        date_pattern = '%Y%m%d-%H%M%S'
        key = 'deploy:{0}:minions'.format(self.repo_name)
        prefix = '{0}'.format(app.config['DEPLOY_DIR'])
        deploy_dir = '{0}/{1}/.git/deploy'.format(prefix, self.repo_name)
        deploy_dir = os.path.abspath(deploy_dir)
        if not os.path.commonprefix([deploy_dir, prefix]).startswith(prefix):
            return
        try:
            f = '{0}/deploy'.format(deploy_dir)
            self.deploy_data = json.loads(open(f).read())
            deploy_time = self.deploy_data['time']
            epoch_time = int(time.mktime(time.strptime(deploy_time,
                                                       date_pattern)))
            self.deploy_data['time'] = epoch_time
        except IOError:
            self.deploy_data = {}
        try:
            f = '{0}/lock'.format(deploy_dir)
            self.lock_data = json.loads(open(f).read())
            lock_time = self.lock_data['time']
            epoch_time = int(time.mktime(time.strptime(lock_time,
                                                       date_pattern)))
            self.lock_data['time'] = epoch_time
        except IOError:
            self.lock_data = {}
        self.minions = redis.smembers(key)
        self.minion_data = {}
        for minion in self.minions:
            key = 'deploy:{0}:minions:{1}'.format(self.repo_name, minion)
            self.minion_data[minion] = redis.hgetall(key)
            # Timestamps are annoyingly strings. We need to fix the injection
            # point to avoid this logic.
            try:
                c_key = 'checkout_timestamp'
                c_ts = self.minion_data[minion][c_key]
                self.minion_data[minion][c_key] = int(float(c_ts))
            except KeyError:
                pass
            try:
                f_key = 'fetch_timestamp'
                f_ts = self.minion_data[minion][f_key]
                self.minion_data[minion][f_key] = int(float(f_ts))
            except KeyError:
                pass

    def get_json(self):
        repo_data = {'deploy_data': self.deploy_data,
                     'minion_data': self.minion_data,
                     'lock_data': self.lock_data}
        return json.dumps(repo_data)


class RepoList(object):

    def __init__(self):
        self.refresh()

    def refresh(self):
        self.repos = redis.smembers('deploy:repos')

    def get_list(self):
        return list(self.repos)
