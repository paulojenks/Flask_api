from flask import Blueprint, abort, url_for

from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with)

import models

# To-Do object Fields
todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


@marshal_with(todo_fields)
def todo_or_404(todos_id):
    """Get the To-Do or give 404 Error"""
    try:
        todo = models.Todo.get(models.Todo.id == todos_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return todo


class TodoList(Resource):
    """To-Do list Class"""
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No To-Do provided...',
            location=['form', 'json']
        )
        super().__init__()

    @staticmethod
    def get():
        """ Get Method for list of to-dos"""
        todos = [marshal(todo, todo_fields) for todo in models.Todo.select()]
        return {'todos': todos}

    @marshal_with(todo_fields)
    def post(self):
        """Post Method for posting a to-do to the list"""
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return todo, 201, {'Location': url_for('resources.todos.todo', id=todo.id)}


class Todo(Resource):
    """To-Do Class"""
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No to-do listed...',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        """Get Method for to-do or give 404 error"""
        return todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        """Put Method to update a To-Do"""
        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        return (models.Todo.get(models.Todo.id == id), 200,
                {'Location': url_for('resources.todos.todo', id=id)}
                )

    @staticmethod
    def delete(id):
        """Delete a single To-do"""
        query = models.Todo.delete().where(models.Todo.id == id)
        query.execute()
        return ('', 204,
                {'Location': url_for('resources.todos.todos')}
                )


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo'
)
