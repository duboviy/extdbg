import sys
import linecache
from traceback import format_exception_only


class CustomExceptHook(object):
    def __init__(self):
        super(CustomExceptHook, self).__init__()
        self._handlers = []

    @property
    def handlers(self):
        return self._handlers

    def __call__(self, exctype, value, traceback):
        for handler in self._handlers:
            handler(exctype, value, traceback)

    def add_handler(self, handler):
        self._handlers.append(handler)

    def remove_handler(self, handler):
        self._handlers.remove(handler)


def excepthook(exctype, value, traceback):
    locals_proc_cache = {}

    def process_var(k, v):
        if k == 'self':
            if id(v) in locals_proc_cache:
                return locals_proc_cache[id(v)]
            res = {'class': v.__class__ .__name__}
            if hasattr(v, 'id'):
                res.update({'id': v.id})
            locals_proc_cache[id(v)] = res
            return res
        return v

    def process_locals(locals_):
        return dict((k, process_var(k, v)) for k, v in locals_.iteritems())

    lines = list()
    lines.append("[TRACEBACK EXT]")
    parent = traceback
    while parent:
        fm = parent.tb_frame
        filename = fm.f_code.co_filename
        lineno = parent.tb_lineno
        name = fm.f_code.co_name
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, fm.f_globals)
        lines.append('  File "%s", line %d, in %s' % (filename, lineno, name))
        lines.append('    ' + line.strip())
        lines.append('    locals: {0}'.format(process_locals(fm.f_locals)))
        parent = parent.tb_next
    lines += [l.strip() for l in format_exception_only(exctype, value)]
    lines.append("[/TRACEBACK EXT]")
    locals_proc_cache = None
    for l in lines:
        print(l)


def init_except_hook():
    # # redundant code
    # gExceptHook = CustomExceptHook()
    # gExceptHook.add_handler(excepthook)

    sys.excepthook = excepthook


if __name__ == '__main__':
    init_except_hook()

    def test(a, b):
        a / b
    test(1, 0)
