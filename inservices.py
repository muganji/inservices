
from datetime import date


from app import app, db
from app.models.user import User
from app.models.usertoken import UserToken
from app.models.websmapuser import WebSmapUser
from app.models.websmapusertoken import WebSmapUserToken
from app.models.recharge import Recharge

@app.shell_context_processor
def make_shell_context():
    return{
        'db': db,
        'User': User,
        'UserToken': UserToken,
        'WebSmapUser': WebSmapUser,
        'WebSmapUserToken': WebSmapUserToken,
        'Recharge': Recharge
    }

@app.context_processor
def inject_current_year():
    return { 'current_year': date.today().year }
