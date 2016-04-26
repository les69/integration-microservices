from flask_restful import Resource

todos = {'hello': 'hello there', 'greetings' : 'goodbye'}


class TestResource(Resource):

    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

