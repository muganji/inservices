from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class WebSmapUser(db.Model):
    """WebSMAP users table
    """    
    __tablename__ = 'websmap_user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)
    can_debit = db.Column(db.Boolean)
    can_credit = db.Column(db.Boolean)

    def set_password(self, password):
        """Creates the password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Checks if password matches the password hash"""
        return check_password_hash(self.password_hash, password)
    
    def valid_username(self):
        return len(WebSmapUser.query.filter_by(username=self.username).all()) < 1
    
    def valid_public_id(self):
        return len(WebSmapUser.query.filter_by(public_id=self.public_id).all()) < 1
