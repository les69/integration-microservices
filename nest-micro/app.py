from flask import Flask, request, abort
from common.integration.nest import NestIntegration, LogInException, NotFoundException
from common.logger.calvinlogger import get_logger
from common.utilities.utils import to_dict

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


@app.route('/device/<deviceid>/<property>/<value>', methods=['PUT'])
def set_value(deviceid, property, value):

    _log.info('{0} {1} {2}'.format(deviceid, property, value))
    success = False
    try:
        nest.check_login()
        success = nest.set_property(deviceid, property, value)

    except LogInException, ex:
        _log.error(ex.message)
        abort(401, ex.message)
    except (NotFoundException, AttributeError), ex:
        _log.error(ex.message)
        abort(404, ex.message)

    return app.response_class(json.dumps({'success': success}), content_type='application/json')


@app.route('/device/<deviceid>/<property>', methods=['GET'])
def get_property(deviceid, property):

    _log.info('{0} {1} '.format(deviceid, property))
    value = None
    try:
        nest.check_login()
        value = nest.get_property(deviceid, property)

    except LogInException, ex:
        _log.error(ex.message)
        abort(401, ex.message)
    except (NotFoundException, AttributeError), ex:
        _log.error(ex.message)
        abort(404, ex.message)

    return app.response_class(json.dumps({'value': value}), content_type='application/json')


@app.route('/device/<deviceid>', methods=['GET'])
def get_device(deviceid):

    _log.info('{0} {1} '.format(deviceid, property))
    device = None

    try:
        nest.check_login()
        device = nest.get_device_by_name(deviceid)

    except LogInException, ex:
        _log.error(ex.message)
        abort(401, ex.message)
    except (NotFoundException, AttributeError), ex:
        _log.error(ex.message)
        abort(404, ex.message)

    js_device = to_dict(device)

    if 'structure' in js_device:
        js_device['structure'] = js_device['structure'].name
    return app.response_class(json.dumps({'device': js_device}), content_type='application/json')


if __name__ == "__main__":
    app.run(port=5001, debug=True)
