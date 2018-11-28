"""accounts routes module.
"""

from app.routes import blueprint_api_accounts


@blueprint_api_accounts.route('/')
def index():
    return 'Hello World'
