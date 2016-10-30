import pickle
import inspect


class func_to_dict(object):
    """
    Converts function of one hashable argument to dictionary-like
    object which "contains" all it returning values.
    """
    def __init__(self, f):
        self.f = f

    def __getitem__(self, key):
        return self.f(key)


def save_object(object_, filename):
    with open(filename, 'w') as f:
        pickle.dump(f, object_)


def load_object(filename):
    with open(filename) as f:
        return pickle.load(f)


def bound_func(func, instance, cls):
    """
    Functions are descriptors,
    so we can bind them by calling their __get__ method.
    """
    return func.__get__(instance, cls)


def run_fn_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


def coroutine(f):
    def wrap(*args,**kwargs):
        gen = f(*args,**kwargs)
        gen.send(None)
        return gen
    return wrap


if __name__ == "__main__":
    # Example of usage
    class Cls2Bound:
        pass

    instance2Bound = Cls2Bound()

    def func(*args, **kwargs):
        print(args, kwargs)

    l = lambda *args, **kwargs: None

    # bound method Cls2Bound.func
    bound_method1 = bound_func(func, instance2Bound, Cls2Bound)
    # bound method Cls2Bound.<lambda>
    bound_method2 = bound_func(l, instance2Bound, Cls2Bound)

    assert inspect.ismethod(bound_method1) == True
    assert inspect.ismethod(bound_method2) == True

    @coroutine
    def calc():
        history = []
        while True:
            x, y = (yield)
            if x == 'h':
                print(history)
                continue
            result = x + y
            print(result)
            history.append(result)


    c = calc()

    assert inspect.isgenerator(c)  # <type 'generator'>

    c.send((1, 2))  # prints 3
    c.send((100, 30))  # prints 130
    c.send((666, 0))  # prints 666
    c.send(('h', 0))  # prints [3, 130, 666]
    c.close()
