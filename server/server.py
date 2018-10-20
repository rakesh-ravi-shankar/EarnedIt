from flask import Blueprint, Flask
from .fitbit_wrapper import fitbitwrap 

blueprint = Blueprint('server', __name__)

@blueprint.route("/")
def index():
    return "Welcome to Earned It!"

@blueprint.route("/fitbittest")
def fitbittest():
	fitbitwrap.authorize()
	return