import unittest
import inspect

import six
from mock import Mock, patch


class TestWhereIs(unittest.TestCase):

    def test_where_is_positive(self):
        expected_filename = "navigate.py"
        expected_line_no = 17

        from extdbg import where_is
        location = where_is(where_is)

        self.assertTrue(isinstance(location.filename, six.string_types))
        self.assertTrue(location.filename.endswith(expected_filename))

        self.assertTrue(isinstance(location.line_no, six.integer_types))
        self.assertEqual(location.line_no, expected_line_no)

    def test_where_is_with_generator(self):
        expected_filename = "test_unit.py"
        expected_line_no = 27

        def g():
            yield 1

        from extdbg import where_is
        location = where_is(g())

        self.assertTrue(isinstance(location.line_no, six.integer_types))
        self.assertEqual(location.line_no, expected_line_no)

        self.assertTrue(isinstance(location.filename, six.string_types))
        self.assertTrue(location.filename.endswith(expected_filename))

    def test_where_is_negative(self):
        expected_filename = None
        expected_line_no = None

        from extdbg import where_is
        location = where_is(frozenset)

        self.assertEqual(location.filename, expected_filename)
        self.assertEqual(location.line_no, expected_line_no)


class TestWatchForOutput(unittest.TestCase):

    def test_works(self):
        from extdbg import watch_for_output

        mock_stdout = Mock()
        output = []

        def write(txt):
            output.append(txt)

        mock_stdout.write = write
        with patch('sys.stdout', mock_stdout):
            watch_for_output(lambda s: 'yes' in s)
            print('yes')

        self.assertIn('yes', output)


class TestExtPPrint(unittest.TestCase):

    def test_works(self):
        from extdbg import pprint

        mock_stdout = Mock()
        output = []

        def write(txt):
            output.append(txt)

        mock_stdout.write = write
        mock_sys = Mock()
        mock_sys.stdout = mock_stdout

        with patch('extdbg.ext_pprint.sys', mock_sys):
            pprint({'a': [1, 2]})

        self.assertEquals(output, [])


class TestBoundFunc(unittest.TestCase):

    def test_works(self):
        from extdbg import bound_func
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

        self.assertTrue(inspect.ismethod(bound_method1))
        self.assertTrue(inspect.ismethod(bound_method2))
