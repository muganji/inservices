import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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

from app.models.recharge import Recharge
from app.models.user import User
from app.models.usertoken import UserToken
from app.models.websmapuser import WebSmapUser
from app.models.websmapusertoken import WebSmapUserToken

from app.api.controllers.accounts.routes import accounts_api
from app.api.controllers.airtime.routes import airtime_api
from app.api.controllers.packages.routes import packages_api
from app.api.controllers.subscribers.routes import subscribers_api

from app.site.developers.accounts.routes import developers_accounts
from app.site.developers.home.routes import developers_home

from app.site.websmap.home.routes import websmap_home
from app.site.websmap.recharges.routes import websmap_recharges

# API
app.register_blueprint(accounts_api, url_prefix='/inservices/api/v1.0/accounts')
app.register_blueprint(airtime_api, url_prefix='/inservices/api/v1.0/airtime')
app.register_blueprint(packages_api, url_prefix='/inservices/api/v1.0/packages')
app.register_blueprint(subscribers_api, url_prefix='/inservices/api/v1.0/profile')

# WebSMAP
app.register_blueprint(websmap_home, url_prefix='/inservices/websmap')
app.register_blueprint(websmap_recharges, url_prefix='/inservices/websmap/recharges')

# developers
app.register_blueprint(developers_accounts, url_prefix='/inservices/developers/accounts')
app.register_blueprint(developers_home, url_prefix='/inservices/developers')

