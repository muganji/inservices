
import uuid
import jwt
from datetime import datetime, timedelta


from flask import (
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


from app import db
from app.models.recharge import Recharge
from app.handlers.websmap import airtime_credit
from app.forms.recharge import RechargeForm
from app.site.websmap import websmap_blueprint

@websmap_blueprint.route('/recharges')
def index():
    return render_template('websmap/recharges/index.html')

@websmap_blueprint.route('/recharges/new', methods=['GET', 'POST'])
@login_required
def new():
    form = RechargeForm()
    if form.validate_on_submit():
        airtime_credit_successful = airtime_credit(
            form.mobile_number.data,
            str(form.amount.data),
            current_user)

        if airtime_credit_successful:
            recharge = Recharge(
                msisdn=form.mobile_number.data,
                amount=form.amount.data)
            db.session.add(recharge)
            db.session.commit()
            flash(f'Airtime recharge on {form.mobile_number.data} of\
             {form.amount.data} was successful')
        else:
            flash('ERROR: Airtime recharge failed!')

        if airtime_credit_successful:
            return redirect(url_for('websmap_recharges.index'))
    return render_template('websmap/recharges/new.html')
