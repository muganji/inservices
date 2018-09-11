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
from app.models import User, UserToken
from app.api.decorators import token_required
from app.api.handlers import store_token, valid_user


websmap_home = Blueprint('websmap_home', __name__, template_folder='templates')

@websmap_home.route('/')
def index():
    return render_template('websmap/home/index.html')
