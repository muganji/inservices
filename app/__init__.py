from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from app.api.controllers.accounts.routes import accounts_api
from app.api.controllers.airtime.routes import airtime_api
from app.api.controllers.packages.routes import packages_api
from app.api.controllers.subscribers.routes import subscribers_api
from app.websmap.controllers.api.airtime.routes import websmap_airtime_api
from app.websmap.controllers.api.accounts.routes import websmap_accounts_api
from app.site.accounts.routes import site_accounts

# Register blueprints
app.register_blueprint(accounts_api, url_prefix='/inservices/api/v1.0/accounts')
app.register_blueprint(airtime_api, url_prefix='/inservices/api/v1.0/airtime')
app.register_blueprint(packages_api, url_prefix='/inservices/api/v1.0/packages')
app.register_blueprint(subscribers_api, url_prefix='/inservices/api/v1.0/profile')

# WEBSMAP blueprints
app.register_blueprint(websmap_airtime_api, url_prefix='/inservices/websmap/api/v1.0/airtime')
app.register_blueprint(websmap_accounts_api, url_prefix='/inservices/websmap/api/v1.0/accounts')

# Site blueprints
app.register_blueprint(site_accounts, url_prefix='/inservices/accounts')

