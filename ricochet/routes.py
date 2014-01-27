from flask import make_response
from flask import json

from ricochet import app
from ricochet import models
from ricochet import auth


@app.route('/')
def index():
    return make_response(open('ricochet/templates/index.html').read())

@app.route('/repolist')
@auth.check_auth
def repolist():
    repos = models.RepoList()

    return json.dumps(repos.get_list())

@app.route('/repo/<path:repo_name>')
@auth.check_auth
def repo(repo_name):
    repo = models.Repo(repo_name)

    return repo.get_json()
