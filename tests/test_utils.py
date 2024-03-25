from io import StringIO
from utils.utils import show
import unittest
import sys


class TestShowFunction(unittest.TestCase):
    def setUp(self):
        self.capturedOutput = StringIO()
        sys.stdout = self.capturedOutput

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_show_with_simple_html(self):
        test_html = "<html><body><p>Hello, World!</p></body></html>"
        expected_output = "Hello, World!"
        show(test_html)
        self.assertEqual(self.capturedOutput.getvalue(), expected_output)

    def test_show_with_nested_html(self):
        test_html = "<div><p>Nested <span>text</span> here.</p></div>"
        expected_output = "Nested text here."
        show(test_html)
        self.assertEqual(self.capturedOutput.getvalue(), expected_output)

    def test_show_with_empty_html(self):
        test_html = "<html><body></body></html>"
        expected_output = ""
        show(test_html)
        self.assertEqual(self.capturedOutput.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
