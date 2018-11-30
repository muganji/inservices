"""Custom decorators module.
"""
from functools import wraps
import jwt

from flask import request, jsonify

from app.handlers.core_handler import transactionid_generator
from app.inservices import app, logger
from app.models.user import User


def token_required(func):
    """Decorator for all routes that require a token.

    Parameters
    ----------
    func : function
        Function to be decorated.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        transaction_id = transactionid_generator()

        logger.info(
            'API - AUDIT - %s - Accessing %s %s',
            transaction_id,
            request.method,
            request.url
        )

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            logger.info(
                'API - AUDIT - %s - Token is missing.',
                transaction_id
            )
            return jsonify({
                'transactionId': transaction_id,
                'operationResult': 'TOKEN IS MISSING'
            }), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']
                ).first()

            if not current_user:
                logger.info(
                    'API - AUDIT - %s - User does not exist.',
                    transaction_id
                )
                return jsonify({
                    'transactionId': transaction_id,
                    'operationResult': 'INVALID USER CREDENTIALS'
                }), 403
        except:
            logger.info(
                'API - AUDIT - %s - Invalid token.',
                transaction_id
            )
            return jsonify({
                'transactionId': transaction_id,
                'operationResult': 'INVALID TOKEN'
            }), 403

        return func(
            current_user,
            transaction_id,
            *args,
            **kwargs)

    return decorated
