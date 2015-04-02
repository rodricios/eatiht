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

import os

import warnings

import _html

import _epub

def fxn():
    warnings.warn("deprecated", DeprecationWarning)


def text_from_epub(filepath, normalize=True):
    """Extract main text from epub file"""
    return _epub.extract_text(filepath, normalize)

def text_from_html(url_string_filepath_or_file):
    """"Extract main text from html source"""
    url = string = filepath = fileobj = url_string_filepath_or_file

    if url.startswith(tuple("http://", "https://")):
        return _html.extract_text(url)

    elif os.path.exists(filepath):
        with open(filepath, 'r') as htmlfile:
            string = htmlfile.read()

    elif isinstance(fileobj, file):
        string = fileobj.read()

    return _html.extract_from_string(string)
