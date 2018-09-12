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


@api_blueprint.route('/packages/buy', methods=['POST'])
@token_required
def buy(current_user):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        data = request.get_json()
        msisdn = data['msisdn']
        package_grade  = data['packageGrade']
        package_type = data['packageType']

        with INConnection(
            server_host, 
            current_user.mml_username, 
            current_user.mml_password, 
            port, 
            buffer_size) as in_connection:
            if in_connection.purchase_package(
                msisdn, 
                package_type, 
                package_grade):
                message, code = (
                    'Purchased package for {}'
                    .format(msisdn), 201)
            else:
                message, code = 'FAILED_BUY_PACKAGE', 201
    except:
        message, code = 'ERROR_PROCESSING_PACKAGE_PURCHASE', 500
    
    return jsonify({'OperationResult': message}), code
