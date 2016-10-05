import pickle


class func_to_dict(object):
    """
    Converts function of one hashable argument to dictionary-like
    object which "contains" all it returning values.
    """
    def __init__(self, f):
        self.f = f

    def __getitem__(self, key):
        return self.f(key)


def save_object(object, filename):
    with open(filename, 'w') as f:
        pickle.dump(f, object)


def load_object(filename):
    with open(filename) as f:
        return pickle.load(f)
