import string
import random

from app.models.user import User


def valid_user(user: User):
    """Checks if user profile is valid and has no conflicts"""
    return (user.valid_username() and user.valid_public_id())


def password_generator(size=6, chars=string.ascii_letters + string.digits):
    """Generates password.

    Parameters
    size : int
        password length.
    chars : str
        Characters in the string.
    """
    return ''.join(random.choice(chars) for i in range(size))
