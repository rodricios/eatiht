import os
from unittest import TestCase

from ..eatiht_v2 import extract, get_parent_xpaths_and_textnodes, get_xpath_frequencydistribution

# Testdata file declarations
RE_SPLIT_VARIOUS_ENDINGS_FILENAME = os.path.join(os.path.dirname(__file__),'assets/regex_various_endings.html')
RE_SPLIT_DOT_ENDINGS_FILENAME = os.path.join(os.path.dirname(__file__),'assets/regex_dot_endings.html')



class TestRegexSplitVariousEndingsInHTML(TestCase):
    def setUp(self):
        self.file = open(RE_SPLIT_VARIOUS_ENDINGS_FILENAME, 'r')

    def tearDown(self):
        self.file.close()

    def test_splits_regex(self):
        sent_xpath_pairs = get_parent_xpaths_and_textnodes(self.file)
        num_of_splits = len(sent_xpath_pairs)
        self.assertEqual(num_of_splits, 9, "\nrequired number of splits: 9\n" +
                         "actual number of splits:   " + str(num_of_splits))


class TestRegexSplitDotEndingsInHTML(TestCase):
    def setUp(self):
        self.file = open(RE_SPLIT_DOT_ENDINGS_FILENAME, 'r')

    def tearDown(self):
        self.file.close()

    def test_splits_regex(self):
        sent_xpath_pairs = get_parent_xpaths_and_textnodes(self.file)
        num_of_splits = len(sent_xpath_pairs)
        self.assertEqual(num_of_splits, 9, "\nrequired number of splits: 9\n" +
                         "actual number of splits:   " + str(num_of_splits))
