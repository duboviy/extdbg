import inspect


class Location(object):
    def __init__(self, filename=None, line_no=None):
        self.filename = filename
        self.line_no = line_no

    def __str__(self):
        return 'At %s:%s' % (
            self.filename or 'unknown',
            self.line_no or 'unknown'
        )
    __repr__ = __str__


def whereis(ob):
    if inspect.isgenerator(ob):
        ob = ob.gi_code
    l = Location()
    try:
        l.filename = inspect.getsourcefile(ob)
    except TypeError:
        pass
    try:
        l.line_no = inspect.getsourcelines(ob)[1]
    except IOError:
        pass
    return l
