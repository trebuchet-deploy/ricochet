from flask import make_response
from flask import json

from ricochet import app
from ricochet import model

@app.route('/')
def index():
    return make_response(open('ricochet/templates/index.html').read())

@app.route('/repolist')
def repolist():
    repos = model.RepoList()

    return json.dumps(repos.get_list())

@app.route('/repo/<path:repo_name>')
def repo(repo_name):
    repo = model.Repo(repo_name)

    return repo.get_json()
