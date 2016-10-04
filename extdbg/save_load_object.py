import pickle


def save_object(object, filename):
    with open(filename, 'w') as f:
        pickle.dump(f, object)


def load_object(filename):
    try:
        with open(filename) as f:
            return pickle.load(f)
    except IOError:
        return None

