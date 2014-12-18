from lxml import html
from collections import Counter
from exceptions import IOError
import re

### This xpath expression effectively queries html text
### nodes that have a string-length greater than 20
text_finder_xpath = '//body//*[not(self::script or self::style or self::i or self::b or self::strong or self::span or self::a)]/text()[string-length(normalize-space()) > 20]/..'

### REGEX patterns for catching bracketted numbers - as seen in wiki articles -
### and sentence splitters
bracket_pattern = re.compile('(\[\d*\])')
#http://stackoverflow.com/questions/8465335/a-regex-for-extracting-sentence-from-a-paragraph-in-python
sentence_token_pattern_A = re.compile(r'''(?<=[.!?]['"\s])\s*(?=[A-Z])''')
#http://stackoverflow.com/questions/25735644/python-regex-for-splitting-text-into-sentences-sentence-tokenizing
sentence_token_pattern_B = re.compile(r'''(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s''')
#http://stackoverflow.com/questions/8465335/a-regex-for-extracting-sentence-from-a-paragraph-in-python
sentence_token_pattern_C = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
          (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        \s+               # Split on whitespace between sentences.
        """,
        re.IGNORECASE | re.VERBOSE)


### Return a frequency distribution over  that gets the most common xpath
def getXPathFrequencyDistribution(paths):
    #split xpath into list of strings
    splitpaths = [p.split('/') for p in paths]

    #get list of "parentpaths" by right-stripping off the last xpath-node, effectively
    #getting the parent path
    parentpaths = ['/'.join(p[:-1]) for p in splitpaths]

    #build frequency distribution
    parentpathsCounter = Counter(parentpaths)
    return parentpathsCounter.most_common()

### Given the url (string), it will download, parse, then iterate through
### text nodes (using xpath), and for each text leafnode, it will build up
### a list of tuples containing the sentence and xpath to said sentence
def getSentencesAndXpaths(url):
    try:
        parsed_html = html.parse(url)
    except IOError as e:
        #workaround for problems in some sites requiring cookies
        #like new york times website
        #http://stackoverflow.com/questions/15148376/urllib2-returning-no-html
        import requests

        page = requests.get(url)

        try:
            from cStringIO import StringIO as BytesIO
        except ImportError:
            from io import BytesIO

        #http://lxml.de/parsing.html
        parsed_html = html.parse( BytesIO(page.content), html.HTMLParser() )

    xpath_finder = parsed_html.getroot().getroottree().getpath

    nodes_with_text = parsed_html.xpath(text_finder_xpath)

    sent_xpath_pairs = [(s, xpath_finder(n))
        for n in nodes_with_text
        #for s in sent_tokenize(re.sub(bracket_pattern,'',''.join(n.xpath('.//text()'))))
        for s in sentence_token_pattern_A.split( re.sub( bracket_pattern, '', ''.join( n.xpath( './/text()') ) ) )
        if s.endswith('.')]

    return sent_xpath_pairs

def extractArticleText(url):
    sent_xpath_pairs = getSentencesAndXpaths(url)

    max_path = getXPathFrequencyDistribution([x for (s,x) in sent_xpath_pairs])[0]

    article_text = ' '.join( [ s for (s,x) in sent_xpath_pairs if max_path[0] in x ])
    #text = ' '.join([d['sent'] for d in sentences])
    return article_text#.encode('latin-1',errors='ignore')
