"""accounts routes module.
"""
import datetime
import uuid

from flask import jsonify, make_response, request
import jwt
from werkzeug.security import check_password_hash

from app import app, db
from app.models.user import User
from app.models.usertoken import UserToken
from app.routes import blueprint_api_accounts


@blueprint_api_accounts.route('/login')
def login():
    '''Login route'''
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(
            'LOGIN CREDENTIALS REQUIRED',
            403,
            {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response(
            'USER DOES NOT EXIST',
            403,
            {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password_hash, auth.password):
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

    return make_response(
        'INVALID USERNAME OR PASSWORD',
        403,
        {'WWW-Authenticate': 'Basic realm="Login required!"'})


@blueprint_api_accounts.route('/create')
def create():
    """Route to create user accounts.
    """
    new_user = User(
        public_id=uuid.uuid4(),
        username='vasuser',
        is_admin=True,
        is_active=True,
        can_debit=True,
        can_credit=True,
        mml_username='pkgmml',
        mml_password='pkgmml99',
        user_type='ADMIN'
    )

    if new_user.is_valid():
        password_generated = new_user.set_password()
        db.session.add(new_user)
        db.session.commit()

        return jsonify(
            {
                'username': new_user.username,
                'password': password_generated
            }
        ), 200
\
    return make_response(
        'USER CREDENTIALS ARE ALREADY TAKEN',
        409
    )
