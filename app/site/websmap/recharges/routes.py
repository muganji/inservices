from flask import (
    jsonify, 
    request, 
    make_response, 
    Blueprint,
    render_template)
from intelecom.intelecom import INConnection
import uuid
import jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta


from app import app, db
from app.models.user import User
from app.models.usertoken import UserToken
from app.decorators import token_required
from app.handlers import store_token, valid_user
from app.forms.recharge import RechargeForm


websmap_recharges = Blueprint('websmap_recharges', __name__, template_folder='templates')

@websmap_recharges.route('/')
def index():
    return render_template('websmap/recharges/index.html')

@websmap_recharges.route('/new', methods=['GET', 'POST'])
def new():
    form = RechargeForm()
    if form.validate_on_submit():
        pass
    return render_template('websmap/recharges/new.html')
