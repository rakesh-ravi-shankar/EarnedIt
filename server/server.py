from flask import Blueprint, Flask

blueprint = Blueprint('server', __name__)

@blueprint.route("/")
def index():
    return "Welcome to Earned It!"