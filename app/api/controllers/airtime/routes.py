from flask import jsonify, request, make_response, Blueprint
from intelecom.intelecom import INConnection
import uuid
import jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta


from app import app, db
from app.models import User, UserToken
from app.api.decorators import token_required
from app.api.handlers import store_token, valid_user


airtime_api = Blueprint('airtime', __name__)


@airtime_api.route('/debit', methods=['POST'])
@token_required
def debit(current_user):
    """Debit airtime account"""
    data = request.get_json()
    msisdn = data['msisdn']
    amount = data['amount']

    with INConnection(
        app.config['IN_SERVER']['HOST'],
        current_user.mml_username,
        current_user.mml_password,
        app.config['IN_SERVER']['PORT'],
        app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:
        if in_connection.debit_account(msisdn, amount, '{0} request'.format(current_user.mml_username)):
            message,code = 'SUCCESS: Airtime debit of amount {0} on MSISDN {1} completed successfully'.format(amount, msisdn),200
        else:
            message,code = 'FAILED_AIRTIME_DEBIT',500
    
    return jsonify({'OperationResult': message}),code

@airtime_api.route('/credit', methods=['POST'])
@token_required
def credit(current_user):
    """Credit airtime account"""
    data = request.get_json()
    msisdn = data['msisdn']
    amount = data['amount']

    with INConnection(
        app.config['IN_SERVER']['HOST'],
        current_user.mml_username,
        current_user.mml_password,
        app.config['IN_SERVER']['PORT'],
        app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:
        if in_connection.credit_account(msisdn, amount, '{0} request'.format(current_user.mml_username)):
            message,code = 'SUCCESS: Airtime credit of amount {0} on MSISDN {1} completed successfully'.format(amount, msisdn),200
        else:
            message,code = 'FAILED_AIRTIME_CREDIT',500
    
    return jsonify({'OperationResult': message}),code
