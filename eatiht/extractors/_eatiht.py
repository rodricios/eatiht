"""eatiht algo"""

import collections

import re

import chardet


try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from lxml import html


BRACKET_PATTERN = re.compile(r'(\[\d*\])')

TEXT_XPATH = '//*[not(self::script or self::style)]/\
                    text()[normalize-space()]/..'

NORM_TEXT_XPRSN = './/*[not(self::script or self::style or self::a or self::figure or self::span)]/text()[normalize-space()]'

SENTENCE_ENDINGS = ['.', '"', '?', '!', "'"]


def _etree_from_string(string):
    """Detect encoding and parse string into lxml's element tree"""

    encoding = chardet.detect(string)['encoding']

    parsed_html = html.parse(BytesIO(string),
                             html.HTMLParser(encoding=encoding,
                                             remove_blank_text=True))

    return parsed_html


def _get_path_textlen_pairs(etree, xpath_to_text=TEXT_XPATH):
    """
    Given a url and xpath, this function will download, parse, then
    iterate though queried text-nodes. From the resulting text-nodes,
    extract a list of (text, exact-xpath) tuples.
    """

    try:
        xpath_finder = etree.getroot().getroottree().getpath

    except(AttributeError):
        xpath_finder = etree.getroottree().getpath

    #for annoying <p><span>...</span></p>
    #https://github.com/rodricios/eatiht/issues/12
    for elem in etree.xpath('//p/span'):
        elem.drop_tag()

    nodes_with_text = etree.xpath(xpath_to_text)

    xpath_textlen_pairs = []

    for node in nodes_with_text:
        #for wikipedia pages ("[12]")
        text = BRACKET_PATTERN.sub('', ''.join(node.xpath(NORM_TEXT_XPRSN)))

        #get path of parent node by rsplit'ing
        #the rsplit'ing logic was moved from get_xpath_frequencydistribution
        xpath_textlen_pairs.append((xpath_finder(node).rsplit('/', 1)[0],
                                    len('\n\n' + text)))

    return xpath_textlen_pairs


def _get_path_textlen_fdistribution(xpath_textlen_pairs):
    """Return Counter object with xpaths-to-textlength
    frequency distribution"""
    histogram = collections.Counter()

    for path, count in xpath_textlen_pairs:
        histogram[path] += count

    return histogram


def _get_content_etree(etree):
    """Calculate the node(s) leading to "main" content"""

    path_count_pairs = _get_path_textlen_pairs(etree)

    path_count_fdist = _get_path_textlen_fdistribution(path_count_pairs)

    path_to_text = path_count_fdist.most_common(1)[0][0]

    return etree.xpath(path_to_text)


def content_from_etree(etree, normalize=True):
    """Eatiht algo for .epub files.
    Optionally normalize all text, removing epub format."""

    global CONTENT_ETREE
    CONTENT_ETREE = content_etree = _get_content_etree(etree)

    assert len(content_etree) is 1

    if normalize:
        content = ' '.join(content_etree[0].xpath(NORM_TEXT_XPRSN))
    else:
        content = ' '.join(content_etree[0].xpath(".//text()"))

    return content
