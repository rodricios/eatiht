import os
from unittest import TestCase

from .. import extract

from .. import extractors

html = extractors._html

THIS_FILE = os.path.dirname(__file__)

FOOS_FILENAME = os.path.join(THIS_FILE, 'assets/full_of_foos.html')

# Testdata file declarations
RE_SPLIT_VARIOUS_ENDINGS_FILENAME = os.path.join(THIS_FILE,'assets/regex_various_endings.html')

RE_SPLIT_DOT_ENDINGS_FILENAME = os.path.join(THIS_FILE,'assets/regex_dot_endings.html')


class TestExtractHtmlString(TestCase):
    def setUp(self):
        self.file = open(FOOS_FILENAME, 'r')
        self.text = self.file.read()

    def tearDown(self):
        self.file.close()

    def test_is_str(self):
        content = html.extract_from_string(self.text)

        print(content)

        self.assertTrue(isinstance(content, str))

    def test_str_is_foos(self, ):
        content = html.extract_from_string(self.text)

        foos = "foo. foo. foo. foo. foo. foo. foo. foo. foo."

        self.assertEqual(content, foos)

    def test_etree_from_url(self, ):
        url = "http://en.wikipedia.org/wiki/Google"

        extracted_etree = html._etree_from_url(url)

        from lxml import etree

        self.assertTrue(isinstance(extracted_etree, etree._ElementTree))
