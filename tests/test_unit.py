import unittest

from extdbg import whereis


class TestWhereis(unittest.TestCase):

    def test_where_is(self):
        location = whereis(whereis)
        self.assertTrue(isinstance(location.line_no, int))
        self.assertTrue(isinstance(location.filename, str))

    def test_with_generator(self):
        def g():
            yield 1

        location = whereis(g())
        self.assertTrue(isinstance(location.line_no, int))
        self.assertTrue(isinstance(location.filename, str))

# TODO: add more tests ASAP!