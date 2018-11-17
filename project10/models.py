import datetime

from peewee import *

DATABASE = SqliteDatabase('todo.sqlite')


class Todo(Model):
    """Create To-Do Model"""
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    """Initialize Database"""
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
