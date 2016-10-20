""" Module allows you to decorate a function in your Python code, making it run in a separate thread. """
import threading


class Threadator(threading.Thread):
    """ See: http://stackoverflow.com/a/25072068 """

    def __init__(self, *args, **kwargs):
        super(Threadator, self).__init__(*args, **kwargs)
        self._return = None

    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)

    def join(self, *args, **kwargs):
        super(Threadator, self).join(*args, **kwargs)
        return self._return


def threaded(daemon=False):
    """ 
    Decorator that runs a callable in a separate thread that can be
    flagged as a 'daemon thread'.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            t = Threadator(target=fn, args=args, kwargs=kwargs)
            t.daemon = daemon
            t.start()
            return t.join()
        return wrapper
    return decorator


if __name__ == "__main__":
    # example of usage
    def fib(n):
        if n < 2:
            return n
        return fib(n-2) + fib(n-1)
    
    print(fib(35))
    
    @threaded(daemon=True)
    def _fib(n):
        if n < 2:
            return n
        return fib(n-2) + fib(n-1)
    
    print(_fib(35))
