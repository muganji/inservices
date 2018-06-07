from app import app
from flask import jsonify, request
from intelecom.intelecom import INConnection

@app.route('/inservices/api/v1.0/profile/<msisdn>')
def profile(msisdn):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        with INConnection(server_host, 'pkgmml', 'pkgmml99', port, buffer_size) as in_connection:
            message, code = in_connection.display_account_info(msisdn), 200

    except:
        message, code = 'FAILED: Request not executed', 500
    
    return jsonify(dict(message)), code

@app.route('/inservices/api/v1.0/buypackage', methods=['POST'])
def buy_package():
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        data = request.get_json()
        msisdn = data['msisdn']
        package_grade  = data['packageGrade']
        package_type = data['packageType']

        with INConnection(server_host, 'pkgmml', 'pkgmml99', port, buffer_size) as in_connection:
            if in_connection.purchase_package(msisdn, package_type, package_grade):
                message, code = 'Purchased package for {}'.format(msisdn), 201
            else:
                message, code = 'FAILED_BUY_PACKAGE', 201
    except:
        message, code = 'ERROR_PROCESSING_PACKAGE_PURCHASE', 500
    
    return jsonify({'result': message}), code

@app.route('/inservices/api/v1.0/changeprofile', methods=['POST'])
def change_profile(parameter_list):
    try:
        server_host = app.config['IN_SERVER']['HOST']
        port = app.config['IN_SERVER']['PORT']
        buffer_size = app.config['IN_SERVER']['BUFFER_SIZE']

        data = request.get_json()
        msisdn = data['msisdn']
        profile = data['profile']

        with INConnection(server_host, 'pkgmml', 'pkgmml99', port, buffer_size) as in_connection:
            if in_connection.change_profile(msisdn, profile):
                message, code = 'Profile for {0} changed to {1}'.format(msisdn, profile), 201
            else:
                message, code = 'FAILED_PROFILE_CHANGE', 201
    except:
        message, code = 'ERROR_CHANGING_PROFILE', 500
    
    return jsonify({'result': message}), code
