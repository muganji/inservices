"""user module
"""
from werkzeug.security import generate_password_hash, check_password_hash

from app.inservices import db, login


@login.user_loader
def load_user(user_id):
    """Load the user profile.

    Parameters
    ----------
    user_id : str
        user ID.
    """
    return User.query.get(int(user_id))


class User(db.Model):
    """Users table"""
    __tablename__ = 'api_user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    can_debit = db.Column(db.Boolean)
    can_credit = db.Column(db.Boolean)
    mml_username = db.Column(db.String(20), unique=True)
    mml_password = db.Column(db.String(20), unique=True)
    virtual_number = db.Column(db.String(20), unique=True)
    user_type = db.Column(db.String(10))

    def set_password(self, password):
        """Creates the password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if password matches the password hash"""
        return check_password_hash(self.password_hash, password)

    def valid_username(self):
        """Checks to make sure that username is unique.
        """
        return len(User.query.filter_by(username=self.username).all()) < 1

    def valid_public_id(self):
        """Checks to make sure that the public id is unique.
        """
        return len(User.query.filter_by(public_id=self.public_id).all()) < 1

    def valid_mml_username(self):
        """Checks if the MML username is unique.
        """
        return len(
            User.query.filter_by(mml_username=self.mml_username).all()) < 1

    def valid_mml_password(self):
        """Checks if the MML password is unique.
        """
        return len(User.query.filter_by(mml_password=self.mml_password).all()) < 1
