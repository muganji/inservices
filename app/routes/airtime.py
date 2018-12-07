"""IN subscriber Airtime Module for crediting and debiting of MSISDN account.
"""

from flask import jsonify, request
from app import app, logger
from app.decorators import token_required
from app.models.user import User
from app.routes import blueprint_api_airtime
from intelecom.intelecom import INQueryError
from app.handlers.profile_handler import INRequestHandler


@blueprint_api_airtime.route('/debit', methods=['POST'])
@token_required
def debit_msisdn(current_user: User, transaction_id: str):
    """Debit the MSISDN account balance.

        Parameters
        ----------
        current_user : User
            User performing the profile debit query.
        transaction_id : str
            Transaction_id number for the debit transaction.

        Returns
        -------
        dict
            Transaction details, account information and the status code.
        """
    data = request.get_json()
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )
    try:
        successful_operation = request_manager.debit_airtime(
            msisdn=data['msisdn'],
            amount=data['amount'],
            current_user=current_user
        )
        debit_response = {
            'transactionId': transaction_id,
            'operationResult': successful_operation['operationResult'],
            'msisdn': successful_operation['msisdn'],
            'amount': successful_operation['amount'],
            'message': 'Debit query successful'
        }
        status_code = 200
        msisdn = successful_operation['msisdn']
        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) debit query SUCCESS - %s',
            transaction_id,
            msisdn,
            current_user.username
        )
    except INQueryError:
        debit_response = {
            'transactionId': transaction_id,
            'operationResult': 'Failed',
            'msisdn': data['msisdn'],
            'amount': None,
            'message': 'Debit query failed'
        }
        status_code = 500
        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) debit query FAILED with IN'
            ' query error - %s',
            transaction_id,
            data['msisdn'],
            current_user.username
        )

    return jsonify(debit_response), status_code


@blueprint_api_airtime.route('/credit', methods=['POST'])
@token_required
def credit_msisdn(current_user: User, transaction_id: str):
    """Credit the MSISDN account balance.

        Parameters
        ----------
        current_user : User
            User performing the profile debit query.
        transaction_id : str
            Transaction_id number for the credit transaction.

        Returns
        -------
        dict
            Transaction details, account information and the status code.
        """
    data = request.get_json()
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )
    try:
        successful_operation = request_manager.credit_airtime(
            msisdn=data['msisdn'],
            amount=data['amount'],
            current_user=current_user
        )
        credit_response = {
            'transactionId': transaction_id,
            'operationResult': successful_operation['operationResult'],
            'msisdn': successful_operation['msisdn'],
            'amount': successful_operation['amount'],
            'message': 'Credit query successful'
        }
        status_code = 200
        msisdn = successful_operation['msisdn']
        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) credit query SUCCESS - %s',
            transaction_id,
            msisdn,
            current_user.username
        )
    except INQueryError:
        credit_response = {
            'transactionId': transaction_id,
            'operationResult': 'Failed',
            'msisdn': data['msisdn'],
            'amount': None,
            'message': 'credit query failed'
        }
        status_code = 500

        logger.info(
            'API - SYSTEM - %s - MSISDN(%s) credit query FAILED with IN'
            ' query error - %s',
            transaction_id,
            data['msisdn'],
            current_user.username
        )
    return jsonify(credit_response), status_code
