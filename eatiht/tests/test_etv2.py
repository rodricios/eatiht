import os
from unittest import TestCase

from ..etv2 import get_html_tree, get_textnode_subtrees

# Testdata file declarations
RE_SPLIT_VARIOUS_ENDINGS_FILENAME = os.path.join(os.path.dirname(__file__),'assets/regex_various_endings.html')
RE_SPLIT_DOT_ENDINGS_FILENAME = os.path.join(os.path.dirname(__file__),'assets/regex_dot_endings.html')



class TestRegexSplitVariousEndingsInHTML(TestCase):
    def setUp(self):
        self.file = open(RE_SPLIT_VARIOUS_ENDINGS_FILENAME, 'r')

    def tearDown(self):
        self.file.close()

    def test_splits_regex(self):
        html_tree = get_html_tree(self.file)

        subtrees = get_textnode_subtrees(html_tree)

        num_of_splits = len(subtrees)
        self.assertEqual(num_of_splits, 9, "\nrequired number of splits: 9\n" +
                         "actual number of splits:   " + str(num_of_splits))


class TestRegexSplitDotEndingsInHTML(TestCase):
    def setUp(self):
        self.file = open(RE_SPLIT_DOT_ENDINGS_FILENAME, 'r')

    def tearDown(self):
        self.file.close()

    def test_splits_regex(self):
        html_tree = get_html_tree(self.file)

        subtrees = get_textnode_subtrees(html_tree)

        num_of_splits = len(subtrees)
        self.assertEqual(num_of_splits, 9, "\nrequired number of splits: 9\n" +
                         "actual number of splits:   " + str(num_of_splits))
