import inspect


class Location(object):
    def __init__(self, filename, line_no):
        self.filename = filename
        self.line_no = line_no

    def __str__(self):
        return 'At %s:%s' % (
            self.filename or 'unknown',
            self.line_no or 'unknown'
        )
    __repr__ = __str__


def where_is(ob):
    if inspect.isgenerator(ob):
        ob = ob.gi_code
    try:
        filename = inspect.getsourcefile(ob)
    except TypeError:
        filename = None
    try:
        line_no = inspect.getsourcelines(ob)[1]
    except TypeError:
        line_no = None
    l = Location(filename, line_no)
    return l
