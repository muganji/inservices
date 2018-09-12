from app import db
from datetime import datetime


class Recharge(db.Model):
    """WebSMAP recharges table"""
    __tablename__ = 'websmap_recharge'

    id = db.Column(db.Integer, primary_key=True)
    msisdn = db.Column(db.String(9))
    recharged = db.Column(db.DateTime, default=datetime.now)
    amount = db.Column(db.Float)
    user_public_id = db.Column(db.String(50))
