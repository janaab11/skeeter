import types
from datetime import datetime, timedelta
from skeeter.logger import logger


def past_timestamp(**kwargs):
    return str(datetime.timestamp(datetime.now() - timedelta(**kwargs)))


def older_than_threshold(ts, threshold=0):
    return True if float(ts) < float(threshold) else False


def clean_url(link):
    return link.replace("&", "&amp;")


def log_exceptions(func):
    """
    Decorator for logging and catching exceptions

    :param func:
    :return:
    """

    def func_wrapper(*args, **kwargs):

        try:
            logger.debug(
                f"Entering method: {func.__name__} with arguments: {args} {kwargs}"
            )
            response = func(*args, **kwargs)
            logger.debug(f"Exiting method: {func.__name__} with response: {response}")
            return response

        except Exception as e:
            logger.exception(e)
            return None

    return func_wrapper


class LogExceptions(type):
    """
    Metaclass that adds decorator to each class method
    """

    def __new__(cls, name, bases, attr):

        for name, value in attr.items():

            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = log_exceptions(value)

        return super(LogExceptions, cls).__new__(cls, name, bases, attr)
