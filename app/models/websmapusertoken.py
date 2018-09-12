from app import db
from datetime import datetime


class WebSmapUserToken(db.Model):
    """WebSMAP user tokens table"""
    __tablename__ = 'websmap_user_token'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    user_public_id = db.Column(db.String(50))
