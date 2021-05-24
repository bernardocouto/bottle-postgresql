from bottle import Bottle, JSONPlugin

import datetime
import decimal
import json


class JSONEncoder(json.JSONEncoder):

    def default(self, entity):
        if isinstance(entity, datetime.date):
            return entity.isoformat()
        if isinstance(entity, datetime.datetime):
            return entity.isoformat()
        if isinstance(entity, decimal.Decimal):
            return float(entity)
        return json.JSONEncoder.default(self, entity)


def application_factory():
    application = Bottle()
    application.install(JSONPlugin(json_dumps=lambda entity: json.dumps(entity, cls=JSONEncoder)))
    return application
