from flask import Blueprint


blueprint_api_profile = Blueprint('blueprint_api_profile', __name__)


@blueprint_api_profile.route('/')
def index():
    return 'Hello World'
