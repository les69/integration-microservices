from flask import Flask, request, abort
from common.integration.nest import NestIntegration, LogInException, NotFoundException
from common.logger.calvinlogger import get_logger

import json

app = Flask(__name__)
_log = get_logger(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
nest = NestIntegration()


@app.route('/login', methods=['POST'])
def login():
    if request.headers['Content-Type'] != 'application/json':
        abort(401)
    _log.info('Request %s' % request.json)
    data = request.json
    success = False

    if nest.login(data['username'], data['password']):
        success = True

    return app.response_class(json.dumps({'login_result': success}), content_type='application/json')


@app.route('/nest/devices', methods=['GET'])
def list_devices():

    try:
        nest.check_login()
    except (LogInException, NotFoundException), ex:
        _log.error(ex.message)
        abort(401, ex.message)

    devices = map(lambda device: device.name, nest.list_devices())
    return app.response_class(json.dumps({'devices': devices}), content_type='application/json')



if __name__ == "__main__":
    app.run(port=5001, debug=True)
