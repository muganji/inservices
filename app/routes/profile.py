
import uuid

from flask import jsonify, make_response, request
from intelecom.intelecom import INQueryError
import jwt

from app import app, db, logger
from app.decorators import token_required
from app.models.user import User
from app.models.usertoken import UserToken
from app.routes import blueprint_api_profile
from app.handlers.profile_handler import INRequestHandler


@blueprint_api_profile.route('/status/<msisdn>', methods=['GET'])
@token_required
def get_msisdn_status(current_user: User, transaction_id: str, msisdn: str):
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )
    try:
        subscriber_info = request_manager.account_info(
            msisdn=msisdn,
            current_user=current_user
        )
        response = {
            'transactionId': transaction_id,
            'operationResult': subscriber_info['operationResult'],
            'msisdn': msisdn,
            'status': subscriber_info['status'],
            'message': 'Status query successful'
        }
        status_code = 200

        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) status query SUCCESS - %s',
            transaction_id,
            msisdn,
            current_user.username
        )
    except INQueryError:
        response = {
            'transactionId': transaction_id,
            'operationResult': 'FAILED',
            'msisdn': msisdn,
            'status': None,
            'message': 'Status query failed'
        }
        status_code = 500

        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) status query FAILED with IN'
            ' query error - %s',
            transaction_id,
            msisdn,
            current_user.username
        )

    return jsonify(response), status_code


@blueprint_api_profile.route('/balance/<msisdn>', methods=['GET'])
@token_required
def get_msisdn_balance(current_user: User, transaction_id: str, msisdn: str):
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )
    try:
        subscriber_balance = request_manager.account_info(
            msisdn=msisdn,
            current_user=current_user
        )
        response = {
            'transactionId': transaction_id,
            'operationResult': subscriber_balance['operationResult'],
            'msisdn': msisdn,
            'balance': subscriber_balance['status'],
            'message': 'Balance query successful'
        }
        status_code = 200

        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) balance query SUCCESS - %s',
            transaction_id,
            msisdn,
            current_user.username
        )
    except INQueryError:
        response = {
            'transactionId': transaction_id,
            'operationResult': 'FAILED',
            'msisdn': msisdn,
            'balance': None,
            'message': 'Balance query failed'
        }
        status_code = 500

        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) balance query FAILED with IN'
            ' query error - %s',
            transaction_id,
            msisdn,
            current_user.username
        )
    return jsonify(response), status_code
