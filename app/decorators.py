from app import app
from flask import request, jsonify
import jwt
from functools import wraps


from app.models.user import User


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
