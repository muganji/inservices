from flask import Blueprint


blueprint_api_airtime = Blueprint('blueprint_api_airtime', __name__)


@blueprint_api_airtime.route('/')
def index():
    return 'Hello World'
