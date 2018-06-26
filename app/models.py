from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """Users table"""
    __tablename__ = 'api_user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    mml_username = db.Column(db.String(20), unique=True)
    mml_password = db.Column(db.String(20), unique=True)

    def set_password(self, password):
        """Creates the password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Checks if password matches the password hash"""
        return check_password_hash(self.password_hash, password)
    
    def valid_username(self):
        return len(User.query.filter_by(username=self.username).all()) < 1
    
    def valid_public_id(self):
        return len(User.query.filter_by(public_id=self.public_id).all()) < 1
    
    def valid_mml_username(self):
        return len(User.query.filter_by(mml_username=self.mml_username).all()) < 1
    
    def valid_mml_password(self):
        return len(User.query.filter_by(mml_password=self.mml_password).all()) < 1

class UserToken(db.Model):
    """User tokens table"""
    __tablename__ = 'api_user_token'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_public_id = db.Column(db.String(50))
