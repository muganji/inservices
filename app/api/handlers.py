from app.models import UserToken
from app import db

def store_token(user_public_id, token):
    """Stores the user token"""
    if user_public_id is not None and token is not None:
        new_token = UserToken(token = token, user_public_id = user_public_id)
        db.session.add(new_token)
        db.session.commit()


def valid_user(user):
    """Checks if user profile is valid and has no conflicts"""
    return (user.valid_username() and user.valid_public_id() and user.valid_mml_username() and user.valid_mml_password())
