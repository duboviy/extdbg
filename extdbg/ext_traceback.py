import sys
import linecache
import logging
from os import linesep
from traceback import format_exception_only


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stderr)
logger.addHandler(handler)


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


def excepthook(exc_type, exc_value, traceback):
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

    traceback_msg = "[Traceback Extended:]" + linesep
    parent = traceback
    while parent:
        fm = parent.tb_frame
        filename = fm.f_code.co_filename
        lineno = parent.tb_lineno
        name = fm.f_code.co_name
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, fm.f_globals)
        traceback_msg += '  File "%s", line %d, in %s' % (filename, lineno, name) + linesep
        traceback_msg += '    ' + line.strip() + linesep
        traceback_msg += '    locals: {0}'.format(process_locals(fm.f_locals)) + linesep
        parent = parent.tb_next
    traceback_msg += ', '.join([l.strip() for l in format_exception_only(exc_type, exc_value)]) + linesep
    traceback_msg += "[/Traceback Extended:]" + linesep
    locals_proc_cache = None
    logger.error(traceback_msg)

    # the original excepthook; don't touch!
    # Handle an exception by displaying it with a traceback on sys.stderr.
    # sys.__excepthook__(exc_type, exc_value, traceback)


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
