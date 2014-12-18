from unittest import TestCase

from ..eatiht import extract, get_sentence_xpath_tuples, get_xpath_frequency_distribution


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
        max_path = get_xpath_frequency_distribution([x for (s,x) in sent_xpath_pairs])[0]
        self.assertTrue(isinstance(max_path, tuple))


class TestExtractArticleText(TestCase):
    def test_is_string(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        text = extract(url)
        self.assertTrue(isinstance(text, basestring))

