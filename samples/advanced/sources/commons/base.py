from bottle import Bottle
from bottle_cerberus import CerberusPlugin
from samples.advanced.sources.commons.singleton import Singleton


class Base(Bottle, metaclass=Singleton):

    def __init__(self):
        super(Base, self).__init__()
        self.install(CerberusPlugin())
