from flask_restful import Resource, fields, marshal_with, reqparse

parser = reqparse.RequestParser()

nest_fields = {
    "device_id": fields.String,
    "structure_id": fields.String,
    "property": fields.String,
    "value": fields.String

}


class Nest(Resource):

    @marshal_with(nest_fields)
    def get(self):
        pass