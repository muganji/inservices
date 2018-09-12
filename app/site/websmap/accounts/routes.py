import uuid
import jwt
from datetime import datetime, timedelta


from flask import (
    jsonify, 
    request, 
    make_response, 
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for)
from intelecom.intelecom import INConnection
from werkzeug.security import generate_password_hash
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required)


from app import app, db
from app.models.recharge import Recharge
from app.decorators import token_required
from app.handlers import store_token, valid_user
from app.forms.recharge import RechargeForm
from app.site.websmap import websmap_blueprint

@websmap_blueprint.route('/accounts/login')
def login():
    pass