import sys
import functools
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def log_invocation(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        logger_ = sys.modules[f.__module__].logger
        logger_.debug('Calling function {} with arguments: args={}, kwargs={}'.format(f.__name__, args, kwargs))
        ret = f(*args, **kwargs)
        logger_.debug('Return value of {} is {}'.format(f.__name__, ret))
        return ret

    return wrapper
