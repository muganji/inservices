from app import app, db
from flask import jsonify, request, make_response
from intelecom.intelecom import INConnection
import jwt
import uuid
from app.models import User, UserToken
from werkzeug.security import generate_password_hash
from functools import wraps
from datetime import datetime, timedelta

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'OperationResult' : 'TOKEN_MISSING'}), 403

        try:
            token_data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=token_data['public_id']).first()
        except:
            return jsonify({'OperationResult' : 'INVALID_TOKEN'}), 403

        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/inservices/api/v1.0/profile/<msisdn>')
@token_required
def profile(current_user, msisdn):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        with INConnection(server_host, current_user.mml_username, current_user.mml_password, port, buffer_size) as in_connection:
            message, code = in_connection.display_account_info(msisdn), 200

    except:
        message, code = 'FAILED_PROFILE_QUERY', 500
    
    return jsonify({'OperationResult': dict(message)}), code

@app.route('/inservices/api/v1.0/buypackage', methods=['POST'])
@token_required
def buy_package(current_user):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        data = request.get_json()
        msisdn = data['msisdn']
        package_grade  = data['packageGrade']
        package_type = data['packageType']

        with INConnection(server_host, current_user.mml_username, current_user.mml_password, port, buffer_size) as in_connection:
            if in_connection.purchase_package(msisdn, package_type, package_grade):
                message, code = 'Purchased package for {}'.format(msisdn), 201
            else:
                message, code = 'FAILED_BUY_PACKAGE', 201
    except:
        message, code = 'ERROR_PROCESSING_PACKAGE_PURCHASE', 500
    
    return jsonify({'OperationResult': message}), code

@app.route('/inservices/api/v1.0/changeprofile', methods=['POST'])
@token_required
def change_profile(current_user):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        data = request.get_json()
        msisdn = data['msisdn']
        profile = data['profile']

        with INConnection(server_host, current_user.mml_username, current_user.mml_password, port, buffer_size) as in_connection:
            if in_connection.change_profile(msisdn, profile):
                message, code = 'Profile for {0} changed to {1}'.format(msisdn, profile), 201
            else:
                message, code = 'FAILED_PROFILE_CHANGE', 201
    except:
        message, code = 'ERROR_CHANGING_PROFILE', 500
    
    return jsonify({'OperationResult': message}), code

@app.route('/inservices/api/v1.0/airtime/debit', methods=['POST'])
@token_required
def debit_airtime(current_user):
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

@app.route('/inservices/api/v1.0/airtime/credit', methods=['POST'])
@token_required
def credit_airtime(current_user):
    """Credit airtime account"""
    data = request.get_json()
    msisdn = data['msisdn']
    amount = data['amount']

    with INConnection(
        app.config['IN_SERVER']['HOST'],
        current_user.mml_username,
        current_user.mml_password,
        app.config['IN_SERVER']['PORT'],
        app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:
        if in_connection.credit_account(msisdn, amount, '{0} request'.format(current_user.mml_username)):
            message,code = 'SUCCESS: Airtime credit of amount {0} on MSISDN {1} completed successfully'.format(amount, msisdn),200
        else:
            message,code = 'FAILED_AIRTIME_CREDIT',500
    
    return jsonify({'OperationResult': message}),code

@app.route('/inservices/api/v1.0/users/create', methods=['POST'])
@token_required
def create_user(current_user):
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

def valid_user(user):
    """Checks if user profile is valid and has no conflicts"""
    return (user.valid_username() and user.valid_public_id() and user.valid_mml_username() and user.valid_mml_password())

def store_token(user_public_id, token):
    """Stores the user token"""
    if user_public_id is not None and token is not None:
        new_token = UserToken(token = token, user_public_id = user_public_id)
        db.session.add(new_token)
        db.session.commit()

