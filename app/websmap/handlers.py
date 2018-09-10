import string
import random

from app.models import WebSmapUserToken
from app import db

def store_token(user_public_id, token):
    """Stores the user token"""
    if user_public_id is not None and token is not None:
        new_token = WebSmapUserToken(token = token, user_public_id = user_public_id)
        db.session.add(new_token)
        db.session.commit()


def valid_user(user):
    """Checks if user profile is valid and has no conflicts"""
    return (user.valid_username() and user.valid_public_id())

def password_generator(size=6, chars=string.ascii_letters + string.digits):
    """
    Returns a string of random characters, useful in generating temporary
    passwords for automated password resets.
    
    size: default=8; override to provide smaller/larger passwords
    chars: default=A-Za-z0-9; override to provide more/less diversity
    
    Credit: Ignacio Vasquez-Abrams
    Source: http://stackoverflow.com/a/2257449
    """
    return ''.join(random.choice(chars) for i in range(size))
