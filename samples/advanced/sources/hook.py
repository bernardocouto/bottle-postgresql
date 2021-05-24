from samples.advanced.sources.commons.singleton import Singleton


def after_request():
    Singleton.clear()


def before_request():
    pass
