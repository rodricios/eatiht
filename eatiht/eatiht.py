"""
eatiht
Extract Article Text In HyperText documents

written by Rodrigo Palacios

**tl;dr**
(revised on 12/20/2014)

Note: for those unfamiliar with xpaths, think of them as file/folder
paths, where each "file/folder" is really just some HTML element.

Algorithm, dammit!:
Using a clever xpath expression that targets the immediate parents of
text nodes of a certain length N, one can get a list of parent nodes
which have, what we can consider as "ideal," text nodes (nodes that
have sentences).

For each text node, we "partition" the text node so that instead of the
parent node having the original text node as its lone child, the parent
now has P children; the partitioning method used is a REGEX sentence
split.

Finally, using now the *parents* of the the above mentioned parent
nodes as our sample, we create a frequency distribution measuring
the number of text node descendants of each parent. In other words,
We can find the xpath with the most number of text node descendants.
This output has shown to lead us to the main article in a webpage.

**A slightly more formal explenation**
(Needs revision as of 12/20/2014)

A reminder: with the help of one of the most fundamental statistical
tools - the frequency distribution - one can easily pick out the
element appearing most frequently in a list of elements.

Now, consider some arbitrary webpage, comprising of stylistic/structural
nodes (div, p, etc.) and "text" nodes (html leafnodes that contain
onscreen text). For every node, there exists at least one XPath that
can describe a leaf node's location within the html tree. If one
assumes some arbitry "sentence length" N and queries for text nodes
that adhere to that constraint (ie. string-length > N), a list of only
text nodes with string length greater than N is returned.

Using those newly-acquired list of nodes, two things must happen for
this algorithm to work properly:

1. Split the text within each text node into sentences (current
implementation relies on REGEX sentence-splitting patterns).

2. For each new pseudo-node that is created upon sentence-split, attach
*not* the xpath that leads to the original text node, but the xpath of
the *parent* node that leads to the original text node.

The last two steps will essentially create a list of (sentence, xpath)
tuples. After this, one can build a frequency distribution across the
xpaths.

Finally, the most frequent element in the freq. distribution (aka
"argmax") should* be the parent node leading to the structural html-element
that "divides" or "encompasses" the main text body.

Please refer to this project's github page for more information:
https://github.com/im-rodrigo/eatiht

Contact the author:
twitter - @mi_ogirdor
email - rodrigopala91@gmail.com
github - https://github.com/im-rodrigo
"""

import re
from collections import Counter
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from lxml import html
import requests


### This xpath expression effectively queries html text
### nodes that have a string-length greater than 20
TEXT_FINDER_XPATH = '//body//*[not(self::script or self::style or self::i or self::b or self::strong or self::span or self::a)]/text()[string-length(normalize-space()) > 20]/..'

### REGEX patterns for catching bracketted numbers - as seen in wiki articles -
### and sentence splitters
bracket_pattern = re.compile('(\[\d*\])')

#http://stackoverflow.com/questions/8465335/a-regex-for-extracting-sentence-from-a-paragraph-in-python
sentence_token_pattern = re.compile(r"""
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
    Given a url and xpath, this function will download, parse, then
    iterate though queried text-nodes. From the resulting text-nodes,
    extract a list of (text, exact-xpath) tuples.
    """
    try:
        parsed_html = html.parse(url)

    except IOError as e:
        # use requests as a workaround for problems in some
        # sites requiring cookies like nytimes.com
        # http://stackoverflow.com/questions/15148376/urllib2-returning-no-html
        page = requests.get(url)

        # http://lxml.de/parsing.html
        parsed_html = html.parse(BytesIO(page.content), html.HTMLParser() )

    xpath_finder = parsed_html.getroot().getroottree().getpath

    nodes_with_text = parsed_html.xpath(xpath_to_text)

    sent_xpath_pairs = [
        ('\n\n' + s, xpath_finder(n)) if e == 0     # hard-code paragraph breaks (there has to be a better way)
        else (s, xpath_finder(n))
        for n in nodes_with_text
        for e, s in enumerate(sentence_token_pattern.split(bracket_pattern.sub('', ''.join(n.xpath('.//text()')))))
        if s.endswith('.') or s.endswith('"') or s.endswith('?')
        ]

    return sent_xpath_pairs


def extract(url, xpath_to_text = TEXT_FINDER_XPATH):
    """
    Wrapper function for extracting the main article from html document.

    A crappy flowchart/state-diagram:
    start: url[,xpath] -> xpaths of text-nodes -> frequency distribution
    -> argmax( freq. dist. ) = likely xpath leading to article's content
    """
    sent_xpath_pairs = get_sentence_xpath_tuples(url, xpath_to_text)

    max_path = get_xpath_frequency_distribution([x for (s,x) in sent_xpath_pairs ])[0]

    article_text = ' '.join([s for (s,x) in sent_xpath_pairs if max_path[0] in x])

    # starting from index 2 because of the two extra newlines in front
    return article_text[2:]
