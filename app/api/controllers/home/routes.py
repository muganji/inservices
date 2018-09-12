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


@api_blueprint.route('/login')
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
            'exp': datetime.utcnow() + timedelta(minutes=5)},
            app.config['SECRET_KEY'])
        store_token(user.public_id, token)
        return jsonify({'Token': token.decode('UTF-8')})
    
    return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm="Login required"'})
