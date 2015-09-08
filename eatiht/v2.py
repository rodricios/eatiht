"""eatiht - Extract Article Text In HyperText documents

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
#from lxml.html.clean import Cleaner TODO!

TEXT_FINDER_XPATH = '//body\
                        //*[not(\
                            self::script or \
                            self::noscript or \
                            self::style or \
                            self::i or \
                            self::em or \
                            self::b or \
                            self::strong or \
                            self::span or \
                            self::a)] \
                            /text()[string-length(normalize-space()) > 20]/..'


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


# same as v1
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


# TODO: rename these funcs to something that makes more sense
def calc_avgstrlen_pathstextnodes(pars_tnodes, dbg=False):
    """In the effort of not using external libraries (like scipy, numpy, etc),
    I've written some harmless code for basic statistical calculations
    """
    ttl = 0
    for _, tnodes in pars_tnodes:
        ttl += tnodes[3]        # index #3 holds the avg strlen

    crd = len(pars_tnodes)
    avg = ttl/crd
    if dbg is True:
        print(avg)
    #       avg = ttl/crd
    return (avg, ttl, crd)


# TODO: rename these funcs to something that makes more sense
def calc_across_paths_textnodes(paths_nodes, dbg=False):
    """Given a list of parent paths tupled with children textnodes, plus
    initialized feature values, we calculate the total and average string
    length of the parent's children textnodes.
    """

    # for (path, [textnodes],
    #           num. of tnodes,
    #           ttl strlen across tnodes,
    #           avg strlen across tnodes.])
    for path_nodes in paths_nodes:
        cnt = len(path_nodes[1][0])
        ttl = sum([len(s) for s in paths_nodes[1][0]])  # calculate total
        path_nodes[1][1] = cnt                          # cardinality
        path_nodes[1][2] = ttl                          # total
        path_nodes[1][3] = ttl/ cnt                     # average
        if dbg:
            print(path_nodes[1])

# TODO: consider changing this name to "get_textnode_subtrees"
# see etv2.
def get_parent_xpaths_and_textnodes(filename_url_or_filelike,
                                    xpath_to_text=TEXT_FINDER_XPATH):
    """Provided a url, path or filelike obj., we construct an html tree,
    and build a list of parent paths and children textnodes & "feature"
    tuples.
    The features - descriptive values used for gathering statistics that
    attempts to describe this artificial environment I've created (parent
    paths and children textnodes) - are initialized to '0'

    Modifications of eatiht.get_sentence_xpath_tuples: some code was
    refactored-out, variable names are slightly different. This function
    does wrap the ltml.tree construction, so a file path, file-like
    structure, or URL is required.
    """
    html_tree = get_html_tree(filename_url_or_filelike)

    xpath_finder = html_tree.getroot().getroottree().getpath

    nodes_with_text = html_tree.xpath(xpath_to_text)

    # read note 5
    parentpaths_textnodes = [
        (xpath_finder(n),
         [n.xpath('.//text()'),   # list of text from textnode
          0,                      # number of texts (cardinality)
          0,                      # total string length in list of texts
          0])                     # average string length
        for n in nodes_with_text
        ]

    if len(parentpaths_textnodes) is 0:
        raise Exception("No text nodes satisfied the xpath:\n\n" +
                        xpath_to_text + "\n\nThis can be due to user's" +
                        " custom xpath, min_str_length value, or both")

    return parentpaths_textnodes


def extract(filename_url_or_filelike):
    """A more precise algorithm over the original eatiht algorithm
    """
    pars_tnodes = get_parent_xpaths_and_textnodes(filename_url_or_filelike)
    #[iterable, cardinality, ttl across iterable, avg across iterable.])
    calc_across_paths_textnodes(pars_tnodes)

    avg, _, _ = calc_avgstrlen_pathstextnodes(pars_tnodes)

    filtered = [parpath_tnodes for parpath_tnodes in pars_tnodes
                if parpath_tnodes[1][2] > avg]

    paths = [path for path, tnode in filtered]

    hist = get_xpath_frequencydistribution(paths)
    try:
        target_tnodes = [tnode for par, tnode in pars_tnodes if hist[0][0] in par]

        target_text = '\n\n'.join([' '.join(tnode[0]) for tnode in target_tnodes])

        return target_text
    except IndexError:
        return ""

def extract_more(filename_url_or_filelike):
    """Does what etv2.extract does, but returns not only the text, but also
    some of the structures that were built along the way:

    results = extract_more(filename_url_or_filelike)

    results[0]      # extracted text

    results[1]      # frequency distribution (histogram)

    results[2]      # subtrees (list of textnodes pre-filter)

    results[3]      # pruned subtrees

    results[4]      # list of paragraphs (as seperated in original website)

    May provide some insight to how this algorithm is calculated, without
    having to read in detail the documentation.
    """
    pars_tnodes = get_parent_xpaths_and_textnodes(filename_url_or_filelike)
    #[iterable, cardinality, ttl across iterable, avg across iterable.])
    calc_across_paths_textnodes(pars_tnodes)

    avg, _, _ = calc_avgstrlen_pathstextnodes(pars_tnodes)

    filtered = [parpath_tnodes for parpath_tnodes in pars_tnodes
                if parpath_tnodes[1][2] > avg]

    paths = [path for path, tnode in filtered]

    hist = get_xpath_frequencydistribution(paths)

    target_tnodes = [tnode for par, tnode in pars_tnodes if hist[0][0] in par]

    target_paras = [' '.join(tnode[0]) for tnode in target_tnodes]

    target_text = '\n\n'.join([' '.join(tnode[0]) for tnode in target_tnodes])

    return (target_text, hist, target_tnodes, filtered, target_paras)
