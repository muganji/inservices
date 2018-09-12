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

def config_app(app):
    config_name = os.getenv('FLASK_ENV', 'default')
    app.config.from_pyfile('config.py')
    app.config.from_object(config_env[config_name])

app = Flask(__name__, instance_relative_config=True)
config_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.blueprint_login_views

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
