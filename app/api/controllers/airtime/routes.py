from flask import jsonify, request, make_response, Blueprint
from intelecom.intelecom import INConnection
import uuid
import jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta


from app import app, db
from app.models.user import User
from app.models.usertoken import UserToken
from app.decorators import token_required
from app.handlers import store_token, valid_user


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
    escrow_account = current_user.virtual_number

    # Open connection to the IN.
    with INConnection(
        app.config['IN_SERVER']['HOST'],
        current_user.mml_username,
        current_user.mml_password,
        app.config['IN_SERVER']['PORT'],
        app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        # Deduct the amount to be credited from escrow account.        
        succeeded_escrow_account_debit = in_connection.debit_account(
            escrow_account, 
            amount, 
            '{0} request'.format(current_user.mml_username))

        # If escrow account deduction is successful.
        if succeeded_escrow_account_debit:
            # Credit the msisdn account.
            account_credit_succeeeded = in_connection.credit_account(
                msisdn, 
                amount, 
                '{0} request'.format(current_user.mml_username))

            # If msisdn credit succeeded return success code.
            if account_credit_succeeeded:
                message,code = 'SUCCESS: Airtime credit of amount {0} on MSISDN {1} completed successfully'.format(amount, msisdn),200
            else:
                message,code = 'FAILED_AIRTIME_CREDIT',500
                reverse_escrow_transaction = in_connection.credit_account(
                    escrow_account,
                    msisdn,
                    f'FAILED: Credit of {msisdn}'
                )

                # Track failed reversal transactions.
                if  reverse_escrow_transaction:
                    pass
                else:
                    message,code = 'FAILED_CREDIT_TRANSACTION_REVERSAL',500
        else:
            message,code = 'FAILED_ESCROW_ACCOUNT_DEBIT',500
    
    return jsonify({'OperationResult': message}),code
