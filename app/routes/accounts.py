"""accounts routes module.
"""
import datetime

from flask import jsonify, make_response, request
import jwt
from werkzeug.security import check_password_hash

# from app.inservices import app, db
from app.models.user import User
from app.models.usertoken import UserToken
from app.routes import blueprint_api_accounts


# @blueprint_api_accounts.route('/login')
# def login():
#     '''Login route'''
#     auth = request.authorization

#     if not auth or not auth.username or not auth.password:
#         return make_response(
#             'Could not verify',
#             403,
#             {'WWW-Authenticate': 'Basic realm="Login required!"'})

#     user = User.query.filter_by(username=auth.username).first()

#     if not user:
#         return make_response(
#             'Could not verify',
#             403,
#             {'WWW-Authenticate': 'Basic realm="Login required!"'})

#     if check_password_hash(user.password, auth.password):
#         utc_now = datetime.datetime.utcnow()
#         expires = utc_now + datetime.timedelta(minutes=30)
#         token = jwt.encode(
#             {'public_id': user.public_id, 'exp': expires},
#             app.config['SECRET_KEY'])

#         generated_token = UserToken(
#             user_public_id=user.public_id,
#             token=token.decode('UTF-8'),
#             created=utc_now)
#         db.session.add(generated_token)
#         db.session.commit()

#         return jsonify({'token': token.decode('UTF-8')})

#     return make_response(
#         'Could not verify',
#         403,
#         {'WWW-Authenticate': 'Basic realm="Login required!"'})
