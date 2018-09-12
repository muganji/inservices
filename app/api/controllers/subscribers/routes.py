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
from app.api import api_blueprint


@api_blueprint.route('/profile/change', methods=['POST'])
@token_required
def change(current_user):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        data = request.get_json()
        msisdn = data['msisdn']
        profile = data['profile']

        with INConnection(
            server_host, 
            current_user.mml_username, 
            current_user.mml_password, 
            port, buffer_size) as in_connection:
            if in_connection.change_profile(msisdn, profile):
                message, code = 'Profile for {0} changed to {1}'.format(msisdn, profile), 201
            else:
                message, code = 'FAILED_PROFILE_CHANGE', 201
    except:
        message, code = 'ERROR_CHANGING_PROFILE', 500
    
    return jsonify({'OperationResult': message}), code


@api_blueprint.route('/profile/<msisdn>')
@token_required
def query(current_user, msisdn):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        with INConnection(server_host, current_user.mml_username, current_user.mml_password, port, buffer_size) as in_connection:
            status, message, code = 'OperationResult', dict(in_connection.display_account_info(msisdn)), 200

    except:
        status, message, code = 'Error', 'FAILED_PROFILE_QUERY', 500
    
    return jsonify({ status: message }), code


@api_blueprint.route('/profile/balance/<msisdn>')
@token_required
def balance(current_user, msisdn):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        with INConnection(server_host, current_user.mml_username, current_user.mml_password, port, buffer_size) as in_connection:
            account_info_dictionary = dict(in_connection.display_account_info(msisdn))
            status,message, code = (
                'Balance',
                account_info_dictionary['ACCLEFT'],
                200)

    except:
        status,message,code = ('Error','FAILED_BALANCE_QUERY', 500)

    
    return jsonify({status: message}), code
