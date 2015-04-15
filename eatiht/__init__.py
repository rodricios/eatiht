"""eatiht - Extract Article Text In HyperText documents

written by Rodrigo Palacios - Copyright 2014

(added on 12/26/2014)

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


(revised on 12/20/2014)

Note: for those unfamiliar with xpaths, think of them as file/folder
paths, where each "file/folder" is really just some HTML element.

Algorithm v1, dammit!:

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


https://github.com/rodricios/eatiht

Contact the author:
twitter - @rodricios
email - rodrigopala91@gmail.com
github - https://github.com/rodricios/eatiht
"""


from .eatiht import extract, get_sentence_xpath_tuples, get_xpath_frequencydistribution
from . import eatiht_trees
from . import etv2
