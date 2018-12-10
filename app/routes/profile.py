
import uuid

from flask import jsonify, make_response, request
import jwt

from app.decorators import token_required
from app import app, logger
from app.models.user import User
from app.models.usertoken import UserToken
from app.routes import blueprint_api_profile
from app.handlers.profile_handler import INRequestHandler


@blueprint_api_profile.route('/balance/<msisdn>')
@token_required
def balance(current_user: User, transaction_id: str, msisdn: str):
    """Get MSISDN balance
    """
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )

    logger.info(
        'API - SYSTEM - %s - BALANCE query for %s  - %s',
        transaction_id,
        msisdn,
        current_user.username
    )

    account_info = request_manager.account_info(msisdn, current_user)
    account_balance = {
        'transactionId': transaction_id,
        'mobileNumber': account_info['mobileNumber'],
        'balance': account_info['mobileNumber'],
    }

    return jsonify(account_balance), 200


@blueprint_api_profile.route('/<msisdn>')
@token_required
def info(current_user: User, transaction_id: str, msisdn: str):
    """Get MSISDN account profile.
    """
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )

    logger.info(
        'API - SYSTEM - %s - PROFILE query for %s  - %s',
        transaction_id,
        msisdn,
        current_user.username
    )

    account_info = request_manager.account_info(msisdn, current_user)
    account_info['transactionId'] = transaction_id

    return jsonify(account_info), 200
