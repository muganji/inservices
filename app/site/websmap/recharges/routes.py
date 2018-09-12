
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

@websmap_blueprint.route('/recharges')
def index():
    return render_template('websmap/recharges/index.html')

@websmap_blueprint.route('/recharges/new', methods=['GET', 'POST'])
def new(current_user):
    form = RechargeForm()
    if form.validate_on_submit():
        recharge = Recharge(
            msisdn=form.mobile_number.data, 
            amount=form.amount.data)
        db.session.add(recharge)
        db.session.commit()
        flash(f'Mobile number: {form.mobile_number.data} recharged\
         amount {form.amount.data} successfully')
        return redirect(url_for('websmap_recharges.index'))
    return render_template('websmap/recharges/new.html')

def credit():
    """Credit airtime account"""
    data = request.get_json()
    msisdn = data['msisdn']
    amount = data['amount']
    user = data['user']

    # Open connection to the IN.
    with INConnection(
        app.config['IN_SERVER']['HOST'],
        current_user.mml_username,
        current_user.mml_password,
        app.config['IN_SERVER']['PORT'],
        app.config['IN_SERVER']['BUFFER_SIZE']) as in_connection:

        account_credit_succeeeded = in_connection.credit_account(
            msisdn, 
            amount, 
            'WEBSMAP_{0}'.format(user))

        # If msisdn credit succeeded return success code.
        if account_credit_succeeeded:
            message,code = 'OK',200
        else:
            message,code = 'FAILED_WEBSMAP_AIRTIME_CREDIT',500
