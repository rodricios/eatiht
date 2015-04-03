"""eatiht algo"""

import collections

import re

import chardet


try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from lxml import html

from lxml.html.clean import clean_html


BRACKET_PATTERN = re.compile(r'(\[\d*\])')

TEXT_XPATH = '//*[not(self::script or self::style)]/\
                    text()[normalize-space()]/..'

NORM_TEXT_XPATH = './/text()[normalize-space()]'

FILTER_NORM_TEXT_XPATH = './/*[not(self::script or self::style or \
                  self::figure or self::span or self::time)]/\
                  text()[normalize-space()]'

SENTENCE_ENDINGS = ['.', '"', '?', '!', "'"]


def _merge_tags_from_etree(etree, selection):
    """Clutch helper function. Inspired by annoying <p><span>...</span></p>.
    Addresses the following issue:
    https://github.com/rodricios/eatiht/issues/12"""
    for elem in etree.xpath(selection):
        elem.drop_tag()


def _remove_duplicates_from_etree(etree):
    """Filter out duplicate text nodes"""
    nodeset = set()

    duplicates = []

    for elem in etree.iter():
        if elem.text is None:
            duplicates.append(elem)
        else:
            #clean text while I'm at it
            elem.text = ' '.join(elem.text.split())

            if elem.text in nodeset:
                duplicates.append(elem)
            else:
                nodeset.add(elem.text)

    for elem in duplicates:
        elem.getparent().remove(elem)

    return nodeset


def _etree_from_string(string, clean=False):
    """Detect encoding and parse string into lxml's element tree"""

    encoding = chardet.detect(string)['encoding']

    parsed_html = html.parse(BytesIO(string),
                             html.HTMLParser(encoding=encoding,
                                             remove_blank_text=True))

    if clean:
        parsed_html = clean_html(parsed_html)

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


    _merge_tags_from_etree(etree, '//p/span')

    nodes_with_text = etree.xpath(xpath_to_text)

    xpath_textlen_pairs = []

    for node in nodes_with_text:
        #for wikipedia pages ("[12]")
        text = BRACKET_PATTERN.sub('', ''.join(node.xpath(NORM_TEXT_XPATH)))

        #get path of parent node by rsplit'ing
        #the rsplit'ing logic was moved from get_xpath_frequencydistribution
        xpath_textlen_pairs.append((xpath_finder(node).rsplit('/', 1)[0],
                                    len(text)))

    return xpath_textlen_pairs


def _get_path_textlen_fdistribution(xpath_textlen_pairs):
    """Return Counter object with xpaths-to-textlength
    frequency distribution"""
    histogram = collections.Counter()

    for path, count in xpath_textlen_pairs:
        histogram[path] += count

    return histogram


def _get_content_etree(etree):
    """Return the element tree leading to "main" content"""

    global PAIRS
    PAIRS = path_count_pairs = _get_path_textlen_pairs(etree)

    global HISTOGRAM
    HISTOGRAM = path_count_fdist = _get_path_textlen_fdistribution(path_count_pairs)

    path_to_text = path_count_fdist.most_common(1)[0][0]

    content_etree = etree.xpath(path_to_text)

    #there should only be one path
    assert len(content_etree) is 1

    return content_etree[0]

def _filter_etree(etree, tags_to_merge=[]):
    """Remove nodes that contain share the same text with other nodes.

    TODO: This behavior should be shortcircuited on pages like wikipedia
    articles.

    Optionally merge tags by providing list of
    xpaths targetting the html elements to have merged with said
    element's parents."""

    if tags_to_merge:
        for tag in tags_to_merge:
            _merge_tags_from_etree(etree, tag)

    _remove_duplicates_from_etree(etree)


def content_from_etree(etree, normalize=True):
    """Eatiht algo. Optionally normalize all text"""

    global CONTENT_ETREE
    CONTENT_ETREE = content_etree = _get_content_etree(etree)

    _filter_etree(content_etree, ["//a"])

    if normalize:
        content = ' '.join(content_etree.xpath(FILTER_NORM_TEXT_XPATH))
    else:
        content = ' '.join(content_etree.xpath(".//text()"))

    return content
