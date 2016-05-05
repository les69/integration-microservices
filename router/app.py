from flask import Flask
from flask_restful import Api
from resources.homekit import HomeKitAccessory, HomeKitDevices

app = Flask(__name__)
api = Api(app)

api.add_resource(HomeKitAccessory, '/homekit/<string:room>/<string:accessory>')
api.add_resource(HomeKitDevices,'/homekit/room/<string:room>/', '/homekit/devices' )


if __name__ == '__main__':
    app.run(debug=True)