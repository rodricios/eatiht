import os
from unittest import TestCase

from ..eatiht import extract, get_sentence_xpath_tuples, get_xpath_frequency_distribution

# Testdata file declarations
RE_SPLIT_VARIOUS_ENDINGS_FILENAME = os.path.join(os.path.dirname(__file__),'assets/regex_various_endings.html')
RE_SPLIT_DOT_ENDINGS_FILENAME = os.path.join(os.path.dirname(__file__),'assets/regex_dot_endings.html')


class TestGetSentencesAndXpaths(TestCase):
    def test_is_list(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        sent_xpath_pairs = get_sentence_xpath_tuples(url)
        self.assertTrue(isinstance(sent_xpath_pairs, list))


class TestGetXPathFrequencyDistribution(TestCase):
    '''def test_is_list(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        sent_xpath_pairs = get_sentence_xpath_tuples(url)
        max_paths = get_xpath_frequency_distribution([x for (s,x) in sent_xpath_pairs])
        self.assertTrue(isinstance(max_paths, list))
    '''
    def test_is_tuple(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        sent_xpath_pairs = get_sentence_xpath_tuples(url)

        xpaths = [x for (s,x) in sent_xpath_pairs]
        max_path = get_xpath_frequency_distribution(xpaths)[0]
        self.assertTrue(isinstance(max_path, tuple))


class TestExtractArticleText(TestCase):
    def test_is_string(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        text = extract(url)
        self.assertTrue(isinstance(text, basestring))


class TestRegexSplitVariousEndingsInHTML(TestCase):
    def setUp(self):
        self.file =  open(RE_SPLIT_VARIOUS_ENDINGS_FILENAME,'r')

    def tearDown(self):
        self.file.close()

    def test_splits_regex(self):
        sent_xpath_pairs = get_sentence_xpath_tuples(self.file)
        num_of_splits = len(sent_xpath_pairs)
        self.assertEqual(num_of_splits,9, "\nrequired number of splits: 9\n" +
                         "actual number of splits:   " + str(num_of_splits))


class TestRegexSplitDotEndingsInHTML(TestCase):
    def setUp(self):
        self.file =  open(RE_SPLIT_DOT_ENDINGS_FILENAME,'r')

    def tearDown(self):
        self.file.close()

    def test_splits_regex(self):
        sent_xpath_pairs = get_sentence_xpath_tuples(self.file)
        num_of_splits = len(sent_xpath_pairs)
        self.assertEqual(num_of_splits,9, "\nrequired number of splits: 9\n" +
                         "actual number of splits:   " + str(num_of_splits))
