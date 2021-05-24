from bottle import request
from samples.advanced.sources.business.entity import EntityBusiness
from samples.advanced.sources.commons.base import Base
from samples.advanced.sources.commons.schema import Schema
from samples.advanced.sources.log import get_logger
from samples.advanced.sources.resources.entity.schema import EntitySchema

import json

logger = get_logger(__name__)

entity_business = EntityBusiness()
entity_resource = Base()


@entity_resource.delete('/api/v1/entity/<id:int>')
def delete_entity(id):
    entity_business.delete_entity(id)


@entity_resource.post('/api/v1/entity', schemas={
    Schema.BODY: EntitySchema()
})
def insert_entity():
    data = dict(request.json)
    entity = entity_business.insert_entity(data.get('field'))
    return json.dumps({'data': entity})


@entity_resource.get('/api/v1/entity')
def select_entity_all():
    entities = entity_business.select_entity_all()
    return json.dumps({'data': entities})


@entity_resource.put('/api/v1/entity/<id:int>', schemas={
    Schema.BODY: EntitySchema()
})
def update_entity(id):
    data = dict(request.json)
    entity = entity_business.update_entity(id, data.get('field'))
    return json.dumps({'data': entity})
