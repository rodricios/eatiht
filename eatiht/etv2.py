"""eatiht v2 - Rodrigo Palacios - Copyright 2014

This version of eatiht v2 is the "script" implementation, where
the result is simply the extracted text; there's also extract_more where
the output is the extracted text plus some of the structures that were
built along the way. Please refer to etv2.py for an almost identical
implementation using the classes declared in eatiht_trees.py; an
explanation to the data structures also exist in that file.

etv2.py has the close to the same logic, maybe one less for loop,
but its return value is a class structure that tries to express
some highlevel structure with the extracted text, as well as the
html wrapping that extracted text. This class will likely have a more
defined, probably dramatically different representation in later releases.

Written by Rodrigo Palacios - Copyright 2014

Note: for those unfamiliar with xpaths, think of them as file/folder
paths, where each "file/folder" is really just some HTML element.

Algorithm v2, dammit!:

This algorithm is small modification to the original. I argue that
it is more "precise" at the cost of extra computations
that may otherwise be unnecessary.

The overall process is similar to v1, but removes the "partitioning"
step (please refer to the eatiht.py for details). What the above step
allowed for was a way to artificially boost subtrees (where the root
had branches/leaves that comprised of text) towards the top. The
boosting score was in proportion to a rough estimate on the # of
sentences in that subtree.

Instead, we rely on the average string length across each branch in a
subtree as the one of two vital calculations in this algorithm. Let's
call this a subtree's "avg branch string length" or ABSL for short.
just mentioned avg score is stored in list, along with the original
textnodes (branches), the total string length across the textnodes, and
the number of textnodes (you'll see me sometimes refer to this as the
"cardinal" or "cardinality").

The second decisive calculation is the average across all subtrees'
average branch string length.
Yes, it's an ugly mouthful, but it's a pretty and simple calculation.
We iterate across our list of subtrees, accruing a total of each subtree's
ABSL, and then calculate the average of that, which I'll refer to as
the AStABSL (avg. subtree avg branch str.len.) or AABSL.

The AABSL value serves as a cutoff threshold used during a filtering pass.

This filtering pass happens post-ABSL-AABSL calculations; for each
subtree, we use the subtree's total subtree string (TSL) length as the
value that's gets measured against the AABSL value; those subtree's
with TSL values higher than the AABSL are kept for one final processing
step. I basically see this as a high-pass filter.

This last step will be familiar to those who know a bit about how the
first algorithm generated its results. In short, we build a frequency
distribution where the key ("bucket" or "bin" when referring to our
distribution as a histogram) is a subtree's root xpath.

That's basically it. Now to address some differences, and also to address
the claim I made towards the top, that this algorithm is more "precise"
than the previous one.

I'm not sure if "precise" is the correct word to use, but I'll go with
it anyways. The resulting histogram has shown to have less overall buckets.
In other words, in the "high-pass" filtering stage, it prunes out many
subtrees where text is likely to not be a part of resulting "body."

Put simply, and with some AI nomenclature, we shrink our state space
dramatically. In other words, to me,

    "smaller state space" === "more precise"
    iff "result is the same as previous algorithm"

That may be circular reasoning, faulty logic, what have you. I'm not
classically trained in this sort of thing so I'd appreciate any insight
as to what exactly it is that I'm doing lol.
"""


import chardet

from collections import Counter

try:
    from cStringIO import StringIO as BytesIO
    from urllib2 import HTTPHandler, HTTPSHandler, build_opener, HTTPCookieProcessor
    from cookielib import CookieJar
except ImportError:
    from io import BytesIO
    from urllib.request import HTTPHandler, HTTPSHandler, build_opener, HTTPCookieProcessor
    from http.cookiejar import CookieJar

from lxml import html
from lxml.html.clean import Cleaner

from .eatiht_trees import TextNodeSubTree, TextNodeTree

# decided to use backslashes for readability?
TEXT_FINDER_XPATH = '//body\
                        //*[not(\
                            self::script or \
                            self::noscript or \
                            self::style or \
                            self::i or \
                            self::b or \
                            self::strong or \
                            self::span or \
                            self::a)] \
                            /text()[string-length(normalize-space()) > 20]/..'

# /u/oliver_newton's suggestion made here:
# http://www.reddit.com/r/Python/comments/2pqx2d/just_made_what_i_consider_my_first_algorithm_and/cn0mubp
HTML_CLEANER = Cleaner(scripts=True, javascript=True, comments=True,
                       style=True, links=True, meta=True, add_nofollow=False,
                       page_structure=False, processing_instructions=True,
                       embedded=True, frames=True, forms=True,
                       annoying_tags=True,
                       remove_tags=["a", "i", "em", "b", "strong", "span"],
                       kill_tags=("noscript", "iframe", "figure"),
                       remove_unknown_tags=True, safe_attrs_only=True)

# Unfortunately, this cleans up a ton of lines of unnecessary text...
SENTENCE_ENDING = ['.', '"', '?', '!', "'"]


# Refactored download and lxml tree instantiation
def get_html_tree(filename_url_or_filelike):
    """From some file path, input stream, or URL, construct and return
    an HTML tree.
    """
    try:
        handler = (
            HTTPSHandler
                if filename_url_or_filelike.lower().startswith('https')
                else HTTPHandler
        )
        cj = CookieJar()
        opener = build_opener(handler)
        opener.add_handler(HTTPCookieProcessor(cj))

        resp = opener.open(filename_url_or_filelike)
    except(AttributeError):
        content = filename_url_or_filelike.read()
        encoding = chardet.detect(content)['encoding']

        parsed_html = html.parse(BytesIO(content),
                                 html.HTMLParser(encoding=encoding,
                                                 remove_blank_text=True))

        return parsed_html
    except(ValueError):
        content = filename_url_or_filelike
        encoding = chardet.detect(content)['encoding']

        parsed_html = html.parse(BytesIO(content),
                                 html.HTMLParser(encoding=encoding,
                                                 remove_blank_text=True))

        return parsed_html

    try:
        content = resp.read()
    finally:
        resp.close()

    encoding = chardet.detect(content)['encoding']

    parsed_html = html.parse(BytesIO(content),
                             html.HTMLParser(encoding=encoding,
                                             remove_blank_text=True))

    return parsed_html


def get_xpath_frequencydistribution(paths):
    """ Build and return a frequency distribution over xpath occurrences."""
    # "html/body/div/div/text" -> [ "html", "body", "div", "div", "text" ]
    splitpaths = [p.rsplit('/', 1) for p in paths]

    # get list of "parentpaths" by right-stripping off the last xpath-node,
    # effectively getting the parent path
    # thanks to eugene-eeo for optimization
    parentpaths = [p[0] for p in splitpaths]

    # build frequency distribution
    parentpaths_counter = Counter(parentpaths)
    return parentpaths_counter.most_common()


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
        print(avg)
    #       avg = ttl/crd
    return (avg, ttl, crd)


def get_textnode_subtrees(html_tree,
                          xpath_to_text=TEXT_FINDER_XPATH):
    """A modification of get_sentence_xpath_tuples: some code was
    refactored-out, variable names are slightly different. This function
    does wrap the ltml.tree construction, so a file path, file-like
    structure, or URL is required.
    """

    try:
        xpath_finder = html_tree.getroot().getroottree().getpath
    except(AttributeError):
        xpath_finder = html_tree.getroottree().getpath

    nodes_with_text = html_tree.xpath(xpath_to_text)

    # Within the TextNodeSubTree construction, the ABSL is calculated
    # refer to eatiht_trees.py
    parentpaths_textnodes = [TextNodeSubTree(n, xpath_finder(n),
                                             n.xpath('.//text()'))
                             for n in nodes_with_text]

    if len(parentpaths_textnodes) is 0:
        raise Exception("No text nodes satisfied the xpath:\n\n" +
                        xpath_to_text + "\n\nThis can be due to user's" +
                        " custom xpath, min_str_length value, or both")

    return parentpaths_textnodes


def extract(filename_url_filelike_or_htmlstring):
    """An "improved" algorithm over the original eatiht algorithm
    """
    html_tree = get_html_tree(filename_url_filelike_or_htmlstring)

    subtrees = get_textnode_subtrees(html_tree)
    #[iterable, cardinality, ttl across iterable, avg across iterable.])

    # calculate AABSL
    avg, _, _ = calcavg_avgstrlen_subtrees(subtrees)

    # "high-pass" filter
    filtered = [subtree for subtree in subtrees
                if subtree.ttl_strlen > avg]

    paths = [subtree.parent_path for subtree in filtered]

    hist = get_xpath_frequencydistribution(paths)

    target_subtrees = [stree for stree in subtrees
                       if hist[0][0] in stree.parent_path]

    title = html_tree.find(".//title")

    return TextNodeTree(title.text_content(), target_subtrees, hist)
