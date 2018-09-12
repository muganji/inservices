from flask import (
    jsonify, 
    request, 
    make_response, 
    Blueprint,
    render_template)
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
from app.site.developers import developers_blueprint

@developers_blueprint.route('/')
def index():
    return render_template('developers/accounts/index.html')


@developers_blueprint.route('/accounts/login')
def login():
    pass

@developers_blueprint.route('/accounts/register', methods=['POST'])
@token_required
def register(current_user):
    """Create a new API user"""
    if not current_user.is_admin:
        return jsonify({'OperationResult': 'ACCESS_DENIED'}),403
    else:
        data = request.get_json()
        new_user = User(
            public_id = str(uuid.uuid4()),
            username = data['username'],
            is_admin = False,
            is_active = True,
            mml_username = data['mml_username'],
            mml_password = data['mml_password']
        )

        if valid_user(new_user):
            new_user.set_password(data['password'])
            try:
                db.session.add(new_user)
                db.session.commit()
                message,code = 'SUCCESS: User created successfully',200
            except:
                message,code = 'FAILED_CREATE_USER',500
        else:
            message,code = 'INVALID_NEW_USER',200
        return jsonify({'OperationResult': message}),code

@developers_blueprint.route('/accounts/initialsetup')
def initialsetup():
    """Initial setup of the api for use"""
    new_user = User(
        public_id=str(uuid.uuid4()),
        username = app.config['INITIAL_SETUP']['ACCOUNT']['USERNAME'],
        is_admin = app.config['INITIAL_SETUP']['ACCOUNT']['IS_ADMIN'],
        is_active = app.config['INITIAL_SETUP']['ACCOUNT']['IS_ACTIVE'],
        can_debit = app.config['INITIAL_SETUP']['ACCOUNT']['CAN_DEBIT'],
        can_credit = app.config['INITIAL_SETUP']['ACCOUNT']['CAN_CREDIT'],
        mml_username = app.config['INITIAL_SETUP']['ACCOUNT']['MML_USERNAME'],
        mml_password = app.config['INITIAL_SETUP']['ACCOUNT']['MML_PASSWORD']
    )

    if valid_user(new_user):
        new_user.set_password(app.config['INITIAL_SETUP']['ACCOUNT']['PASSWORD'])
        try:
            db.session.add(new_user)
            db.session.commit()
            message,code = 'SUCCESS_INITIAL_SETUP',200
        except:
            message,code = 'FAILED_INITIAL_SETUP',500
    else:
        message,code = 'OK_INITIAL_SETUP',200
    return jsonify({'OperationResult': message}),code
