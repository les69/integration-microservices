from flask_restful import Resource
from flask import session

import requests


class NestLogin(Resource):

    def get(self):
        res = session['test']
        return {'res': 'lol'}

    def post(self):
        pass
