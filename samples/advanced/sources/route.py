from bottle import Bottle
from samples.advanced.sources.log import get_logger
from samples.advanced.sources.resources.entity.resource import entity_resource

logger = get_logger(__name__)

route = Bottle()

resources = [
    entity_resource
]

for resource in resources:
    route.merge(resource)
