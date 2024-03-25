import unittest
from models.url import URL


class TestURLClass(unittest.TestCase):
    def test_http_scheme(self):
        url = URL("http://example.com")
        self.assertEqual(url.scheme, "http")
        self.assertEqual(url.host, "example.com")
        self.assertEqual(url.path, "/")

    def test_https_scheme(self):
        url = URL("https://example.com")
        self.assertEqual(url.scheme, "https")
        self.assertEqual(url.host, "example.com")
        self.assertEqual(url.path, "/")

    def test_file_scheme(self):
        url = URL("file:///path/to/file")
        self.assertEqual(url.scheme, "file")
        self.assertEqual(url.path, "/path/to/file")

    def test_invalid_scheme(self):
        with self.assertRaises(AssertionError):
            URL("invalid://example.com")

if __name__ == "__main__":
    unittest.main()
