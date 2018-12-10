"""accounts routes module.
"""
import datetime
import uuid

from flask import jsonify, make_response, request
import jwt

from app import app, db, logger
from app.decorators import token_required
from app.models.user import User
from app.models.usertoken import UserToken
from app.routes import blueprint_api_accounts


@blueprint_api_accounts.route('/login')
def login():
    '''Login route'''
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        logger.warning('API - AUDIT - login credentials required.')
        return make_response(
            'LOGIN CREDENTIALS REQUIRED',
            403,
            {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        logger.warning(
            'API - AUDIT - user does not exist (username=%s, password=%s)',
            auth.username,
            auth.password
        )
        return make_response(
            'USER DOES NOT EXIST',
            403,
            {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if user.check_password(auth.password):
        utc_now = datetime.datetime.utcnow()
        expires = utc_now + datetime.timedelta(minutes=30)
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': expires},
            app.config['SECRET_KEY'])

        generated_token = UserToken(
            user_public_id=user.public_id,
            token=token.decode('UTF-8'),
            created=utc_now)
        db.session.add(generated_token)
        db.session.commit()

        return jsonify({'token': token.decode('UTF-8')}), 200

    logger.warning(
        'API - AUDIT - invalid login credentials for %s sent'
        ' (username=%s, password=%s)',
        repr(user),
        auth.username,
        auth.password
    )
    return make_response(
        'INVALID USERNAME OR PASSWORD',
        403,
        {'WWW-Authenticate': 'Basic realm="Login required!"'})


@blueprint_api_accounts.route('/accounts/create', methods=['POST'])
@token_required
def create(current_user: User, transaction_id: str):
    """Route to create user accounts.
    """
    if not current_user.is_admin or not current_user.is_active:
        logger.warning(
            'API - AUDIT - %s - Access denied - %s',
            transaction_id,
            current_user.username
        )
        return jsonify(
            {
                'transactionId': transaction_id,
                'operationResult': 'FORBIDDEN: You do not have the '
                                   'permission to perform operation.'
            }
        ), 403

    data = request.get_json()
    new_user = User(
        public_id=uuid.uuid4(),
        username=data['Username'],
        is_admin=data['IsAdmin'],
        is_active=data['IsActive'],
        can_debit=data['CanDebit'],
        can_credit=data['CanCredit'],
        mml_username=data['MmlUsername'],
        mml_password=data['MmlPassword'],
        user_type=data['UserType']
    )

    if new_user.is_valid():
        password_generated = new_user.set_password()
        db.session.add(new_user)
        db.session.commit()

        logger.info(
            'API - SYSTEM - %s - created %s - %s',
            transaction_id,
            repr(new_user),
            current_user.username
        )
        return jsonify(
            {
                'username': new_user.username,
                'password': password_generated
            }
        ), 200

    logger.info(
        'API - SYSTEM - %s - User already exists %s - %s',
        transaction_id,
        repr(new_user),
        current_user.username
    )
    return jsonify(
        {
            'transactionId': transaction_id,
            'operationResult': 'NEW USER CREDENTIALS ALREADY TAKEN'
        }
    ), 409
