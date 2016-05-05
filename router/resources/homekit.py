from flask_restful import Resource, reqparse, fields, marshal_with
import requests
import json

#fix it using the one in settings.py
HOMEKIT = "http://localhost:5001/homekit"


parser = reqparse.RequestParser()

homekit_fields = {
    "accessory": fields.String,
    "room": fields.String,
    "service": fields.String,
    "characteristic": fields.String,
    "value": fields.String,
    "selector": fields.String

}


class HomeKitAccessory(Resource):

    def get(self,room, accessory):

        url = "{0}/services/{1}/{2}".format(HOMEKIT, room, accessory)
        res = requests.get(url)
        return res.json() if res.content != '' else {'error', res.status_code}

    def post(self):
        #[TODO] add the possibility to add services
        pass


class HomeKitDevices(Resource):

    def get(self, room= None):

        if room is None:
            url = "/devices"
        else:
            url = "{0}/room/{1}/devices".format(HOMEKIT, room)

        res = requests.get(url)
        return res.json() if res.content != '' else {'error', res.status_code}


class HomeKitService(Resource):

    def get(self, room, accessory, service):


        url = "{0}/properties/{1}/{2}/{3}".format(HOMEKIT, room, accessory, service)
        res = requests.get(url)
        return res.json() if res.content != '' else {'error', res.status_code}


class HomeKitAttribute(Resource):

    def get(self, room, accessory, service, attribute):
        url = "{0}/device/{1}/{2}/{3}/{4}".format(HOMEKIT, room, accessory, service, attribute)
        res = requests.get(url)
        return res.json() if res.content != '' else {'error', res.status_code}


    @marshal_with(homekit_fields)
    def post(self):
        pass