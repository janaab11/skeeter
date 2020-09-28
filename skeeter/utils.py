from datetime import datetime, timedelta


def past_timestamp(**kwargs):
    return str(datetime.timestamp(datetime.now() - timedelta(**kwargs)))


def older_than_threshold(ts, threshold=0):
    return True if float(ts) < float(threshold) else False


def clean_url(link):
    return link.replace("&", "&amp;")


def handle_exceptions(func):
    """
    Decorator for func that handles exceptions and prints them
    """

    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None

    return func_wrapper


def handle_exceptions_for_class(Cls):
    """
    Class decorator
    """

    class NewCls(object):
        def __init__(self, *args, **kwargs):
            self.oInstance = Cls(*args, **kwargs)

        def __getattribute__(self, s):
            """
            this is called whenever any attribute of a NewCls object is accessed. This function first tries to
            get the attribute off NewCls. If it fails then it tries to fetch the attribute from self.oInstance (an
            instance of the decorated class). If it manages to fetch the attribute from self.oInstance, and
            the attribute is an instance method then `time_this` is applied.
            """
            try:
                x = super(NewCls, self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(s)
            if type(x) == type(self.__init__):  # it is an instance method
                return handle_exceptions(
                    x
                )  # this is equivalent of just decorating the method with time_this
            else:
                return x

    return NewCls
