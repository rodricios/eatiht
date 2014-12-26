"""eatiht v2 - Rodrigo Palacios - Copyright 2014"""


import urllib2
from collections import Counter
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from lxml import html
from lxml.html.clean import Cleaner

from etv2_textnode_subtree import TextNodeSubTree


TEXT_FINDER_XPATH = '//body \
                        //text() \
                            [string-length(normalize-space()) > 20] \
                            /..'

HTML_CLEANER = Cleaner(scripts=True, javascript=True, comments=True,
                       style=True, links=True, meta=True, add_nofollow=False,
                       page_structure=False, processing_instructions=True,
                       embedded=True, frames=True, forms=True,
                       annoying_tags=True,
                       remove_tags=["a", "i", "em", "b", "strong", "span"],
                       kill_tags=("noscript", "iframe", "figure"),
                       remove_unknown_tags=True, safe_attrs_only=True)


# Refactored download and lxml tree instantiation
def get_html_tree(filename_url_or_filelike):
    """From some file path, input stream, or URL, construct and return
    an HTML tree.
    """
    try:
        parsed_html = html.parse(filename_url_or_filelike,
                                 html.HTMLParser(encoding="utf-8",
                                                 remove_blank_text=True))

    except IOError:
        # use requests as a workaround for problems in some
        # sites requiring cookies like nytimes.com
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(filename_url_or_filelike).read()

        # http://lxml.de/parsing.html
        parsed_html = html.parse(BytesIO(response),
                                 html.HTMLParser(encoding="utf-8",
                                                 remove_blank_text=True))

    # http://www.reddit.com/r/Python/comments/2pqx2d/just_made_what_i_consider_my_first_algorithm_and/cn0mvku
    # thanks for the suggestion /u/oliver_newton
    HTML_CLEANER(parsed_html)

    return parsed_html


def get_xpath_frequencydistribution(paths):
    """ Build and return a frequency distribution over xpath occurrences."""
    # "html/body/div/div/text" -> [ "html", "body", "div", "div", "text" ]
    splitpaths = [p.split('/') for p in paths]

    # get list of "parentpaths" by right-stripping off the last xpath-node,
    # effectively getting the parent path
    parentpaths = ['/'.join(p[:-1]) for p in splitpaths]

    # build frequency distribution
    parentpaths_counter = Counter(parentpaths)
    return parentpaths_counter.most_common()


# read note 2
def calcavg_avgstrlen_subtrees(subtrees, dbg=False):
    """In the effort of not using external libraries (like scipy, numpy, etc),
    I've written some harmless code for basic statistical calculations
    """
    ttl = 0
    for subtree in subtrees:
        ttl += subtree.avg_strlen

    crd = len(subtrees)
    avg = ttl/crd
    if dbg is True:
        print avg
    #       avg = ttl/crd
    return (avg, ttl, crd)


# read note 4
def get_textnode_subtrees(filename_url_or_filelike,
                          xpath_to_text=TEXT_FINDER_XPATH):
    """A modification of get_sentence_xpath_tuples: some code was
    refactored-out, variable names are slightly different. This function
    does wrap the ltml.tree construction, so a file path, file-like
    structure, or URL is required.
    """
    html_tree = get_html_tree(filename_url_or_filelike)

    xpath_finder = html_tree.getroot().getroottree().getpath

    nodes_with_text = html_tree.xpath(xpath_to_text)

    # read note 5
    parentpaths_textnodes = [TextNodeSubTree(xpath_finder(n),
                                             n.xpath('.//text()'))
                             for n in nodes_with_text]

    if len(parentpaths_textnodes) is 0:
        raise Exception("No text nodes satisfied the xpath:\n\n" +
                        xpath_to_text + "\n\nThis can be due to user's" +
                        " custom xpath, min_str_length value, or both")

    return parentpaths_textnodes


def extract(filename_url_or_filelike):
    """An "improved" algorithm over the original eatiht algorithm
    """
    subtrees = get_textnode_subtrees(filename_url_or_filelike)
    #[iterable, cardinality, ttl across iterable, avg across iterable.])

    avg, _, _ = calcavg_avgstrlen_subtrees(subtrees)

    filtered = [subtree for subtree in subtrees
                if subtree.ttl_strlen > avg]
    #filtered = list( filter(pars_tnodes, lambda x: x[1][2] > avg ))

    paths = [subtree.parent_path for subtree in filtered]

    hist = get_xpath_frequencydistribution(paths)

    target_subtrees = [stree for stree in subtrees
                       if hist[0][0] in stree.parent_path]

    target_paras = [' '.join(subtree.text_nodes) for subtree in target_subtrees]

    target_text = '\n'.join([' '.join(subtree.text_nodes)
                             for subtree in target_subtrees])

    return (target_subtrees, target_paras, target_text, hist)
