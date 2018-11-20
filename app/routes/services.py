from flask import Blueprint


blueprint_api_services = Blueprint('blueprint_api_services', __name__)


@blueprint_api_services.route('/')
def index():
    return 'Hello World'
