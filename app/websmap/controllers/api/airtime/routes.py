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


websmap_airtime_api = Blueprint('websmap_airtime', __name__)


@websmap_airtime_api.route('/debit', methods=['POST'])
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

@websmap_airtime_api.route('/credit', methods=['POST'])
@token_required
def credit(current_user):
    """Credit airtime account"""
    data = request.get_json()
    msisdn = data['msisdn']
    amount = data['amount']
    user = data['user']

    # Open connection to the IN.
    with INConnection(
        app.config['IN_SERVER']['HOST'],
        current_user.mml_username,
        current_user.mml_password,
        app.config['IN_SERVER']['PORT'],
        app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        account_credit_succeeeded = in_connection.credit_account(
            msisdn, 
            amount, 
            'WEBSMAP_{0}'.format(user))

        # If msisdn credit succeeded return success code.
        if account_credit_succeeeded:
            message,code = 'OK',200
        else:
            message,code = 'FAILED_WEBSMAP_AIRTIME_CREDIT',500
    
    return jsonify({'OperationResult': message}),code
