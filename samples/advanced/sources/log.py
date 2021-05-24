from samples.advanced.sources.utils import environment

import logging
import logging.config

__logger__ = {}


def get_logger(module):
    global __logger__
    if module not in __logger__:
        logger = logging.getLogger(module)
        logger.setLevel(logging.DEBUG if environment.APPLICATION_DEBUG else logging.WARNING)
        __logger__[module] = logger
    return __logger__[module]
