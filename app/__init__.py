import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


import config


config_env = {
    'default': 'config.default.Config',
    'development': 'config.development.DevelopmentConfig',
    'production': 'config.production.ProductionConfig',
    'testing': 'config.testing.TestingConfig'
}

def config_app(application):
    config_name = os.getenv('FLASK_ENV', 'default')
    application.config.from_pyfile('config.py')
    application.config.from_object(config_env[config_name])

app = Flask(__name__, instance_relative_config=True)
config_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app.models.recharge import Recharge
from app.models.user import User
from app.models.usertoken import UserToken

from app.api import api_blueprint
from app.site.developers import developers_blueprint
from app.site.websmap import websmap_blueprint

# api blueprint
app.register_blueprint(api_blueprint, url_prefix='/inservices/api/v1.0')

# WebSMAP blueprint
app.register_blueprint(websmap_blueprint, url_prefix='/inservices/websmap')

# developers blueprint
app.register_blueprint(developers_blueprint, url_prefix='/inservices/developers')

# Load the user profile
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login.blueprint_login_views = {
    'api_blueprint': '/inservices/api/v1.0/login',
    'developers_blueprint': '/inservices/developers/accounts/login',
    'websmap_blueprint': '/inservices/websmap/accounts/login'
}
