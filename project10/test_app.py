from unittest import TestCase, main

import json

from peewee import *

import app
import models

BASE_URL = '127.0.0.1:5000/api/v1/todos'

DATABASE = SqliteDatabase(':memory:')


class TestProjectApi(TestCase):
    def setUp(self):
        self.app = app.app
        self.app.testing = True
        self.client = self.app.test_client()
        self.todo_test_data = {'name': 'Pick up Orange Juice'}

        DATABASE.connect()
        DATABASE.create_tables([models.Todo], safe=True)

    def test_api_get_todos(self):
        resp = self.client.post('/api/v1/todos', data=self.todo_test_data)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/api/v1/todos')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Pick up Orange Juice', str(resp.data))

    def test_api_get_todo_by_id(self):
        resp = self.client.post('/api/v1/todos', data=self.todo_test_data)
        self.assertEqual(resp.status_code, 201)
        json_results = json.loads(resp.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            '/api/v1/todos/{}'.format(json_results['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Pick up Orange Juice', str(result.data))

    def test_api_edit_todo(self):
        resp = self.client.post('/api/v1/todos', data={'name': 'Drink all the Orange Juice'})
        self.assertEqual(resp.status_code, 201)
        resp = self.client.put('/api/v1/todos/{}'.format(models.Todo.select().get().id),
                               data={'name': 'Put down Orange Juice'})
        self.assertEqual(resp.status_code, 200)
        results = self.client.get('/api/v1/todos/{}'.format(models.Todo.select().get().id))
        self.assertIn('Put down Orange Juice', str(results.data))

    def test_api_delete_todo(self):
        resp = self.client.post('/api/v1/todos', data=self.todo_test_data)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.delete('/api/v1/todos/2')
        self.assertEqual(resp.status_code, 204)
        result = self.client.get('/api/v1/todos/2')
        self.assertEqual(result.status_code, 404)

    def test_todos_view(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        """tearDown method
        - delete tables
        - close database
        """
        DATABASE.drop_tables(models.Todo)
        DATABASE.close()


if __name__ == "__main__":
    main()
