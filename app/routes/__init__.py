"""Routes package initializer
"""
from flask import Blueprint

blueprint_api_accounts = Blueprint('blueprint_api_accounts', __name__)
blueprint_api_airtime = Blueprint('blueprint_api_airtime', __name__)
blueprint_api_profile = Blueprint('blueprint_api_profile', __name__)