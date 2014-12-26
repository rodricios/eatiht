"""eatiht - Extract Article Text In HyperText documents

Written by Rodrigo Palacios - Copyright 2014

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
"""

import urllib2
from collections import Counter
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from lxml import html
from lxml.html.clean import Cleaner


TEXT_FINDER_XPATH = '//body \
                        //text() \
                            [string-length(normalize-space()) > 20] \
                            /..'

HTML_CLEANER = Cleaner(scripts=True, javascript=True, comments=True,
                       style=True, links=True, meta=True, add_nofollow=False,
                       page_structure=False, processing_instructions=True,
                       embedded=True, frames=True, forms=True,
                       annoying_tags=True,
                       remove_tags=["a", "i", "em", "b", "strong"],
                       kill_tags=("noscript", "iframe", "figure"),
                       remove_unknown_tags=True, safe_attrs_only=True)


# Refactored download and lxml tree instantiation
def get_html_tree(filename_url_or_filelike):
    """From some file path, input stream, or URL, construct and return
    an HTML tree.
    """
    try:
        parsed_html = html.parse(filename_url_or_filelike,
                                 html.HTMLParser(encoding="utf-8"))

    except IOError:
        # use requests as a workaround for problems in some
        # sites requiring cookies like nytimes.com
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(filename_url_or_filelike).read()

        # http://lxml.de/parsing.html
        parsed_html = html.parse(BytesIO(response),
                                 html.HTMLParser(encoding="utf-8"))

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
def calc_avgstrlen_pathstextnodes(pars_tnodes, dbg=False):
    """In the effort of not using external libraries (like scipy, numpy, etc),
    I've written some harmless code for basic statistical calculations
    """
    ttl = 0
    for _, tnodes in pars_tnodes:
        ttl += tnodes[3]

    crd = len(pars_tnodes)
    avg = ttl/crd
    if dbg is True:
        print avg
    #       avg = ttl/crd
    return (avg, ttl, crd)


# read note 3
def calc_across_paths_textnodes(paths_nodes,
                                ttlfunc=lambda x: \
                                        sum([len(s) for s in x]),
                                dbg=False):
    """"simplicity" becomes muddled here. But in essence, provided some
    dict-like structure (list of tuple(key,val)), we calculate the total and
    average of some iterable value in each value, and store calculation
    in the element next to original iterated value.
    """

    # for (key, [iterable,
    #           cardinality,
    #           ttl across iterable,
    #           avg across iterable.])
    for path_nodes in paths_nodes:
        cnt = len(path_nodes[1][0])
        ttl = ttlfunc(path_nodes[1][0])
        path_nodes[1][1] = cnt                      # cardinality
        path_nodes[1][2] = ttl                      # total
        path_nodes[1][3] = ttl/ cnt                 # average
        if dbg:
            print path_nodes[1]


# read note 4
def get_parent_xpaths_and_textnodes(filename_url_or_filelike,
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
    """An "improved" algorithm over the original eatiht algorithm
    """
    pars_tnodes = get_parent_xpaths_and_textnodes(filename_url_or_filelike)
    #[iterable, cardinality, ttl across iterable, avg across iterable.])
    calc_across_paths_textnodes(pars_tnodes)

    avg, _, _ = calc_avgstrlen_pathstextnodes(pars_tnodes)

    filtered = [parpath_tnodes for parpath_tnodes in pars_tnodes
                if parpath_tnodes[1][2] > avg]
    #filtered = list( filter(pars_tnodes, lambda x: x[1][2] > avg ))

    paths = [path for path, tnode in filtered]

    hist = get_xpath_frequencydistribution(paths)

    target_tnodes = [tnode for par, tnode in pars_tnodes if hist[0][0] in par]

    target_paras = [' '.join(tnode[0]) for tnode in target_tnodes]

    target_text = '\n'.join([' '.join(tnode[0]) for tnode in target_tnodes])

    return (target_tnodes, target_paras, target_text, hist)

# my ramblings as the algorithm was being written - feel free to disregard
# note 1
# borrowing "peas in a pod" idiom
# To force one's self to not waste calculated information
# and to acquire an intuition for the hierarchical
# structure in statistical calculations, you will
# be forced to accept that more and more values
# in calls such as these
# ie. calc_card     -> [] -> int
# ie. calc_total    -> [] -> int
# ie. calc_average  -> [] -> int,int,int
# ie. calc_variance -> [] -> int,int,int,int
#
# ... will result in more than one output.
# If you call a avg. calculating function,
# you will have to make room for the total and
# cardinal value of the set (just len(set))
#
# I hope that this has a net positive effect on building
# some sort of intuition.

# note 2
# be aware that there are two versions of this:
# this one will take the sum over the avg string length that was
# per parent of textnodes, that is to say the following
#
# ...
#
# parent -> <div>
#      child -> <p>Foobar</p>
#      child -> <p>foo</p>
#      child -> <p>bar</p>
#           </div>
# ...
#
# We have the avg string length over the parent node's children (textnode);
# in this case it's : (6 + 3 + 3)/3 = 12/3 = 4 char's per textnode
# And we have a list of these structures that contain this average value
# (what in machine learning nomenclature is referred to "features"),
# we simply find the avg over those avgs.

# note 3
# statistics for statistics sake requires a bit of unmodality
# consider this: provide me some statistics on such and such?
# if input is a list of complex structs, i argue that there
# should be only one iterable structure in the complex struct
# type:
# [([a,b,c],"item1"),([a,c,e]),"item2",...]
# what this allows for is an overall implicit "dict" type structure
# why not just employ a dict? good questions...
# if we do imagine we are dealing with a dict-like structure,
# we can then push the above mentioned restriction to the
# "value" of a "key":
# [( ( [a,b,c], feat1, feat2 ),"1"),( ( [a,c,e], feat1, feat2 ),"2"),...]
#
# thus, statistics can be applied iterable structure in the tuple
# like structure, and store "features" (numbers that describing
# the iterable structure)
#
# a few obvious things to include in results (feats) are:
# cardinality (if list of lists)
# total across some measurement of iterable
# avg. across some measurement of iterable

# note 4
# these long names will eventually become annoying
# consider abbreviating?

# note 5
# consider abbr. to tnodes_parpaths
# actually, consider being straight up and calling this:
# texts_parentpaths
# textnodes is probably easier to imagine as a part of some tree
# vs. a just "texts"
