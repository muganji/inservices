from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    BooleanField,
    FloatField,
    DateTimeField)
from wtforms.validators import DataRequired, ValidationError


class RechargeForm(FlaskForm):
    mobile_number = StringField('Mobile number', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
