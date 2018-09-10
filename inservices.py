from app import app, db
from app.models import User, UserToken
from datetime import date

@app.shell_context_processor
def make_shell_context():
    return{
        'db': db,
        'User': User,
        'UserToken': UserToken
    }

@app.context_processor
def inject_current_year():
    return { 'current_year': date.today().year }
