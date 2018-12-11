"""IN subscriber Profile Module for balance and status queries of MSISDN account
"""

from flask import jsonify
from intelecom.intelecom import INQueryError

<<<<<<< HEAD
from app import app, logger
from app.decorators import token_required
=======
from flask import jsonify, make_response, request
import jwt

from app.decorators import token_required
from app import app, logger
>>>>>>> upstream/master
from app.models.user import User
from app.routes import blueprint_api_profile
from app.handlers.profile_handler import INRequestHandler


<<<<<<< HEAD
@blueprint_api_profile.route('/status/<msisdn>', methods=['GET'])
@token_required
def get_msisdn_status(current_user: User, transaction_id: str, msisdn: str):
    """Get the MSISDN account Status.

        Parameters
        ----------
        current_user : User
            User performing the profile debit query.
        transaction_id : str
            Transaction_id number for the debit transaction.
        msisdn: str
            MSISDN number for the account whose status is queried.

        Returns
        -------
        dict
            Transaction details, account status and the status code.
        """
=======
@blueprint_api_profile.route('/balance/<msisdn>')
@token_required
def balance(current_user: User, transaction_id: str, msisdn: str):
    """Get MSISDN balance
    """
>>>>>>> upstream/master
    request_manager = INRequestHandler(
        host=app.config['IN_SERVER']['HOST'],
        port=app.config['IN_SERVER']['PORT'],
        buffer_size=app.config['IN_SERVER']['BUFFER_SIZE']
    )
<<<<<<< HEAD
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
    """Get the MSISDN account balance.

        Parameters
        ----------
        current_user : User
            User performing the profile debit query.
        transaction_id : str
            Transaction_id number for the debit transaction.
        msisdn: str
            MSISDN number for the account whose balance is queried.

        Returns
        -------
        dict
            Transaction details, account balance and the status code.
        """
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
            'balance': subscriber_balance['balance'],
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
=======

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
        'balance': account_info['balance'],
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
>>>>>>> upstream/master
