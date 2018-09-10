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


accounts_api = Blueprint('accounts', __name__)

@accounts_api.route('/register', methods=['POST'])
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

@app.route('/inservices/api/v1.0/initialsetup')
def initialsetup():
    """Initial setup of the api for use"""
    new_user = User(
        public_id=str(uuid.uuid4()),
        username = app.config['INITIAL_SETUP']['ACCOUNT']['USERNAME'],
        is_admin = app.config['INITIAL_SETUP']['ACCOUNT']['IS_ADMIN'],
        is_active = app.config['INITIAL_SETUP']['ACCOUNT']['IS_ACTIVE'],
        can_credit = app.config['INITIAL_SETUP']['ACCOUNT']['CAN_CREDIT'],
        can_debit = app.config['INITIAL_SETUP']['ACCOUNT']['CAN_DEBIT'],
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

@app.route('/inservices/api/v1.0/login')
def login():
    """Login and get authentication token"""
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm="Login required'})
    
    user = User.query.filter_by(username=auth.username).first()
    
    if not user:
        return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm="Login required"'})
    
    if user.check_password(auth.password):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        store_token(user.public_id, token)
        return jsonify({'Token': token.decode('UTF-8')})
    
    return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm="Login required"'})
