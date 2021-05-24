from bottle import response, run
from samples.advanced.sources.application import application_factory
from samples.advanced.sources.domains.database import Database
from samples.advanced.sources.hook import after_request, before_request
from samples.advanced.sources.log import get_logger
from samples.advanced.sources.route import route
from samples.advanced.sources.utils import environment

logger = get_logger(__name__)

application = application_factory()
application.add_hook('after_request', after_request)
application.add_hook('before_request', before_request)
application.merge(route)

Database.configuration()


@application.hook('after_request')
def content_type():
    response.content_type = 'application/json; charset=utf-8'


def server():
    run(
        app=application,
        debug=environment.APPLICATION_DEBUG,
        host=environment.APPLICATION_HOST,
        port=environment.APPLICATION_PORT,
        reloader=environment.APPLICATION_RELOADER
    )


if __name__ == '__main__':
    server()
