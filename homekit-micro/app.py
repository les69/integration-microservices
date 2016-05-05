from flask import Flask, request, abort
from common.integration.nest import NestIntegration, LogInException, NotFoundException
from common.logger.calvinlogger import get_logger
from common.utilities.utils import to_dict
import requests

from common.utilities.settings import HOMEKIT_URL


import json

app = Flask(__name__)
_log = get_logger(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
nest = NestIntegration()


@app.route('/homekit/devices', methods=['GET'])
def list_devices():
    try:
        res = requests.get("{0}/{1}".format(HOMEKIT_URL,"devices"))
    except (LogInException, NotFoundException), ex:
        _log.error(ex.message)
        abort(401, ex.message)

    toret = res.json() if res.content != '' else {"error": "error"}
    return app.response_class(json.dumps(toret), content_type='application/json')

@app.route('/homekit/<room_name>/devices', methods=['GET'])
def list_room_devices(room_name):

    try:
        res = requests.get("{0}/{1}/{2}".format(HOMEKIT_URL,"room", room_name))
        print res.json()
    except (LogInException, NotFoundException), ex:
        _log.error(ex.message)
        abort(401, ex.message)

    toret = res.json() if res.content != '' else {"error": "error"}
    return app.response_class(json.dumps(toret), content_type='application/json')

@app.route('/homekit/property/<room>/<accessory>/<service>/<property>', methods=['POST'])
def set_value(room, accessory, service, property):

    value = request.json["value"]
    try:
        res = requests.post("{0}/property/{1}/{2}/{3}/{4}".format(HOMEKIT_URL, room, accessory, service, property), json= {"value": value})

    except LogInException, ex:
        _log.error(ex.message)
        abort(401, ex.message)
    except (NotFoundException, AttributeError), ex:
        _log.error(ex.message)
        abort(404, ex.message)
    toret = res.json() if res.content != '' else {"error": "error"}
    return app.response_class(json.dumps(toret), content_type='application/json')


@app.route('/homekit/device/<room>/<accessory>/<service>/<property>', methods=['GET'])
def get_property(room, accessory, service, property):

    try:
        res = requests.get("{0}/property/{1}/{2}/{3}/{4}".format(HOMEKIT_URL, room, accessory, service, property))

    except LogInException, ex:
        _log.error(ex.message)
        abort(401, ex.message)
    except (NotFoundException, AttributeError), ex:
        _log.error(ex.message)
        abort(404, ex.message)

    toret = res.json() if res.content != '' else {"error": "error"}
    return app.response_class(json.dumps(toret), content_type='application/json')


@app.route('/homekit/properties/<room>/<accessory>/<service>/', methods=['GET'])
def get_attributes(room, accessory, service):

    try:
        res = requests.get("{0}/attributes/{1}/{2}/{3}".format(HOMEKIT_URL, room, accessory, service))
    except LogInException, ex:
        _log.error(ex.message)
        abort(401, ex.message)
    except (NotFoundException, AttributeError), ex:
        _log.error(ex.message)
        abort(404, ex.message)

    toret = res.json() if res.content != '' else {"error": "error"}
    return app.response_class(json.dumps(toret), content_type='application/json')

@app.route('/homekit/services/<room>/<accessory>/', methods=['GET'])
def get_services(room, accessory):

    try:
        res = requests.get("{0}/services/{1}/{2}/".format(HOMEKIT_URL, room, accessory))

    except LogInException, ex:
        _log.error(ex.message)
        abort(401, ex.message)
    except (NotFoundException, AttributeError), ex:
        _log.error(ex.message)
        abort(404, ex.message)

    toret = res.json() if res.content != '' else {"error": "error"}
    return app.response_class(json.dumps(toret), content_type='application/json')




if __name__ == "__main__":
    app.run(port=5001, debug=True)
