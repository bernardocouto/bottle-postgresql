from bottle import Bottle, JSONPlugin, request, response, run
from bottle_postgresql import Configuration, Database

import datetime
import decimal
import json
import os


class JSONEncoder(json.JSONEncoder):

    def default(self, entity):
        if isinstance(entity, datetime.date):
            return entity.isoformat()
        if isinstance(entity, datetime.datetime):
            return entity.isoformat()
        if isinstance(entity, decimal.Decimal):
            return float(entity)
        return json.JSONEncoder.default(self, entity)


application = Bottle()
application.install(JSONPlugin(json_dumps=lambda entity: json.dumps(entity, cls=JSONEncoder)))

configuration_dict = {
    'connect_timeout': os.environ.get('DATABASE_CONNECTION_TIMEOUT'),
    'dbname': os.environ.get('DATABASE_NAME'),
    'host': os.environ.get('DATABASE_HOST'),
    'maxconnections': os.environ.get('DATABASE_MAX_CONNECTION'),
    'password': os.environ.get('DATABASE_PASSWORD'),
    'port': os.environ.get('DATABASE_PORT'),
    'print_sql': os.environ.get('DATABASE_PRINT_SQL'),
    'user': os.environ.get('DATABASE_USERNAME')
}

configuration = Configuration(configuration_dict=configuration_dict)


def connect():
    return Database(configuration)


@application.hook('after_request')
def content_type():
    response.content_type = 'application/json; charset=utf-8'


@application.delete('/api/v1/entity/<id:int>')
def delete(id):
    with connect() as connection:
        entities = (
            connection
            .delete('entities')
            .where('id', id, operator='=')
            .execute()
        )
    return json.dumps({'data': entities})


@application.get('/api/v1/entity')
def find_all():
    with connect() as connection:
        entities = (
            connection
            .select('entities')
            .execute()
            .fetch_all()
        )
    return json.dumps({'data': entities})


@application.post('/api/v1/entity')
def save():
    data = dict(request.json)
    with connect() as connection:
        entities = (
            connection
            .insert('entities')
            .set('field', data.get('field'))
            .execute()
            .fetch_one()
        )
    return json.dumps({'data': entities})


@application.put('/api/v1/entity/<id:int>')
def update(id):
    data = dict(request.json)
    with connect() as connection:
        entities = (
            connection
            .update('entities')
            .set('field', data.get('field'))
            .where('id', id, operator='=')
            .execute()
            .fetch_one()
        )
    return json.dumps({'data': entities})


def server():
    run(
        app=application,
        debug=True,
        host='0.0.0.0',
        port=8080,
        reloader=True
    )


if __name__ == '__main__':
    server()
