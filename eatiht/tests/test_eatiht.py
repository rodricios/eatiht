from unittest import TestCase

from ..eatiht import extractArticleText, getSentencesAndXpaths, getXPathFrequencyDistribution


class TestGetSentencesAndXpaths(TestCase):
    def test_is_list(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        sent_xpath_pairs = getSentencesAndXpaths(url)
        self.assertTrue(isinstance(sent_xpath_pairs, list))


class TestGetXPathFrequencyDistribution(TestCase):
    '''def test_is_list(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        sent_xpath_pairs = getSentencesAndXpaths(url)
        max_paths = getXPathFrequencyDistribution([x for (s,x) in sent_xpath_pairs])
        self.assertTrue(isinstance(max_paths, list))
    '''
    def test_is_tuple(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        sent_xpath_pairs = getSentencesAndXpaths(url)
        max_path = getXPathFrequencyDistribution([x for (s,x) in sent_xpath_pairs])[0]
        self.assertTrue(isinstance(max_path, tuple))


class TestExtractArticleText(TestCase):
    def test_is_string(self):
        url = 'http://en.wikipedia.org/wiki/Google'
        text = extractArticleText(url)
        self.assertTrue(isinstance(text, basestring))

