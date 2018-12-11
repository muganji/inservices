import uuid

from flask import jsonify, make_response, request
import jwt

from app import app, db, logger
from app.decorators import token_required
from app.models.user import User
from app.routes import blueprint_api_airtime
from app.handlers.profile_handler import INRequestHandler


@blueprint_api_airtime.route('/debit', methods=['POST'])
@token_required
def debit_msisdn(current_user: User, transaction_id: str):
    data = request.get_json()
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )

    successful_operation = request_manager.debit_airtime(
        msisdn=data['msisdn'],
        amount=data['amount'],
        current_user=current_user
    )
    if successful_operation:
        debit_response = {
            'transactionalId': transaction_id,
            'operationalResult': 'OK',
            'msisdn': data['msisdn'],
            'amount': data['amount']
        }
        status_code = 200

        logger.info(
            'API - SYSTEM - %s - SUCCESS debit of airtime %s from %s  - %s',
            transaction_id,
            data['amount'],
            data['msisdn'],
            current_user.username
        )
    else:
        debit_response = {
            'transactionalId': transaction_id,
            'operationalResult': 'FAILED',
            'msisdn': data['msisdn'],
            'amount': data['amount']
        }
        status_code = 400

        logger.warning(
            'API - SYSTEM - %s - FAILED debit of airtime %s from %s  - %s',
            transaction_id,
            data['amount'],
            data['msisdn'],
            current_user.username
        )

    return jsonify(debit_response), status_code


@blueprint_api_airtime.route('/credit', methods=['POST'])
@token_required
def credit_msisdn(current_user: User, transaction_id: str):
    data = request.get_json()
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )
    successful_operation = request_manager.credit_airtime(
        msisdn=data['msisdn'],
        amount=data['amount'],
        current_user=current_user
    )
    if successful_operation:
        credit_response = {
            'transactionalId': transaction_id,
            'operationalResult': 'OK',
            'msisdn': data['msisdn'],
            'amount': data['amount']
        }
        status_code = 200

        logger.info(
            'API - SYSTEM - %s - SUCCESS credit of airtime %s from %s  - %s',
            transaction_id,
            data['amount'],
            data['msisdn'],
            current_user.username
        )
    else:
        credit_response = {
            'transactionalId': transaction_id,
            'operationalResult': 'FAILED',
            'msisdn': data['msisdn'],
            'amount': data['amount']
        }
        status_code = 400

        logger.warning(
            'API - SYSTEM - %s - FAILED credit of airtime %s from %s  - %s',
            transaction_id,
            data['amount'],
            data['msisdn'],
            current_user.username
        )
    return jsonify(credit_response), status_code