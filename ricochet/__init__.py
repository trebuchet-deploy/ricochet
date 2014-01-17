from flask import Flask
from flask import make_response

app = Flask(__name__)

import ricochet.routes

