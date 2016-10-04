import unittest

from extdbg import where_is


class TestWhereis(unittest.TestCase):

    def test_where_is_positive(self):
        expected_filename = "navigate.py"
        expected_line_no = 17

        location = where_is(where_is)

        self.assertTrue(isinstance(location.filename, str))
        self.assertTrue(location.filename.endswith(expected_filename))

        self.assertTrue(isinstance(location.line_no, int))
        self.assertEqual(location.line_no, expected_line_no)

    def test_where_is_with_generator(self):
        expected_filename = "test_unit.py"
        expected_line_no = 24

        def g():
            yield 1

        location = where_is(g())

        self.assertTrue(isinstance(location.line_no, int))
        self.assertEqual(location.line_no, expected_line_no)

        self.assertTrue(isinstance(location.filename, str))
        self.assertTrue(location.filename.endswith(expected_filename))

    def test_where_is_negative(self):
        expected_filename = None
        expected_line_no = None

        location = where_is(frozenset)

        self.assertEqual(location.filename, expected_filename)
        self.assertEqual(location.line_no, expected_line_no)

# TODO: add more tests ASAP!