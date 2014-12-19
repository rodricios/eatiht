"""
eatiht
Extract Article Text In HyperText documents

written by Rodrigo

With the help of one of the most basic statistical tools - the frequency distribution -
one can retrieve the argmax (the element appearing the most frequent). Now, if the
element you are measuring the frequency of are XPaths leading to text-nodes (sentences),
one can approximate an XPath that will likely lead to the bulk of the article's text.

Please refer to this project's github page for more information:
https://github.com/im-rodrigo/eatiht

Contact the author:
twitter - @mi_ogirdor
email - rodrigopala91@gmail.com
github - https://github.com/im-rodrigo
"""

from lxml import html
from collections import Counter
from exceptions import IOError
import re

### This xpath expression effectively queries html text
### nodes that have a string-length greater than 20
TEXT_FINDER_XPATH = '//body//*[not(self::script or self::style or self::i or self::b or self::strong or self::span or self::a)]/text()[string-length(normalize-space()) > 20]/..'

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


def get_xpath_frequency_distribution(paths):
    """
    Build and return a frequency distribution over xpath occurrences.
    """
    # "html/body/div/div/text" -> [ "html", "body", "div", "div", "text" ]
    splitpaths = [p.split('/') for p in paths]

    # get list of "parentpaths" by right-stripping off the last xpath-node, effectively
    # getting the parent path
    parentpaths = ['/'.join(p[:-1]) for p in splitpaths]

    # build frequency distribution
    parentpathsCounter = Counter(parentpaths)
    return parentpathsCounter.most_common()


def get_sentence_xpath_tuples(url, xpath_to_text = TEXT_FINDER_XPATH):
    """
    Given a url and xpath, this function will download, parse, then iterate though
    queried text-nodes. From the resulting text-nodes, extract a list of (text, exact-xpath) tuples.
    """
    try:
        parsed_html = html.parse(url)

    except IOError as e:
        # workaround for problems in some sites requiring cookies
        # like nytimes.com
        # http://stackoverflow.com/questions/15148376/urllib2-returning-no-html
        import requests

        page = requests.get(url)

        try:
            from cStringIO import StringIO as BytesIO
        except ImportError:
            from io import BytesIO

        # http://lxml.de/parsing.html
        parsed_html = html.parse( BytesIO(page.content), html.HTMLParser() )

    xpath_finder = parsed_html.getroot().getroottree().getpath

    nodes_with_text = parsed_html.xpath(xpath_to_text)

    sent_xpath_pairs = [(s, xpath_finder(n))
        for n in nodes_with_text
        for s in sentence_token_pattern_C.split( bracket_pattern.sub( '', ''.join( n.xpath( './/text()') ) ) )
        if s.endswith('.')]

    return sent_xpath_pairs


def extract(url, xpath_to_text = TEXT_FINDER_XPATH):
    """
    Wrapper function for extracting the main article from html document
    url[,xpath] -> xpaths of text-paths -> frequency distribution -> argmax( freq. dist. ) = likely xpath leading to article's content
    """
    sent_xpath_pairs = get_sentence_xpath_tuples(url, xpath_to_text)

    max_path = get_xpath_frequency_distribution([x for (s,x) in sent_xpath_pairs])[0]

    article_text = ' '.join( [ s for (s,x) in sent_xpath_pairs if max_path[0] in x ])

    return article_text
