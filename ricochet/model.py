import redis
import time

from flask import json

# TODO (ryan-lane): Make this configurable and move this somewhere sane
serv = redis.Redis(host='localhost', port=6379, db=0)


class Repo(object):

    def __init__(self, repo_name):
        self.repo_name = repo_name;
        self._load_data()

    def _load_data(self):
        date_pattern = '%Y%m%d-%H%M%S'
        key = 'deploy:{0}:minions'.format(self.repo_name)
        try:
            f = '/srv/deployment/{0}/.git/deploy/deploy'.format(self.repo_name)
            self.deploy_data = json.loads(open(f).read())
            deploy_time = self.deploy_data['time']
            epoch_time = int(time.mktime(time.strptime(deploy_time,
                                                       date_pattern)))
            self.deploy_data['time'] = epoch_time
        except IOError:
            self.deploy_data = {}
        try:
            f = '/srv/deployment/{0}/.git/deploy/lock'.format(self.repo_name)
            self.lock_data = json.loads(open(f).read())
            lock_time = self.lock_data['time']
            epoch_time = int(time.mktime(time.strptime(lock_time,
                                                       date_pattern)))
            self.lock_data['time'] = epoch_time
        except IOError:
            self.lock_data = {}
        self.minions = serv.smembers(key)
        self.minion_data = {}
        for minion in self.minions:
            key = 'deploy:{0}:minions:{1}'.format(self.repo_name, minion)
            self.minion_data[minion] = serv.hgetall(key)
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
        self.repos = serv.smembers('deploy:repos')

    def get_list(self):
        return list(self.repos)
