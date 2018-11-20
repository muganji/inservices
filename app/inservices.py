import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.routes.accounts import blueprint_api_accounts
from app.routes.airtime import blueprint_api_airtime
from app.routes.profile import blueprint_api_profile
from app.routes.services import blueprint_api_services


app = Flask(__name__, instance_relative_config=True)

CONFIG_ENV = {
    'default': 'config.default.Config',
    'development': 'config.development.DevelopmentConfig',
    'production': 'config.production.ProductionConfig',
    'testing': 'config.testing.TestingConfig'
}


def config_app(application):
    """Application configuration function.

    Parameters
    ----------
    application: Flask
        Flask application to configure.
    """
    config_name = os.getenv('FLASK_ENV', 'default')
    application.config.from_pyfile('config.py')
    application.config.from_object(CONFIG_ENV[config_name])


app = Flask(__name__, instance_relative_config=True)
config_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# api blueprints
app.register_blueprint(
    blueprint_api_accounts,
    url_prefix='/inservices/api/v1.0/accounts'
)
app.register_blueprint(
    blueprint_api_airtime,
    url_prefix='/inservices/api/v1.0/airtime'
)
app.register_blueprint(
    blueprint_api_profile,
    url_prefix='/inservices/api/v1.0/profile'
)
app.register_blueprint(
    blueprint_api_services,
    url_prefix='/inservices/api/v1.0/services'
)
