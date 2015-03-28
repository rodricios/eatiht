eatiht
======

A python package for **e**\ xtracting **a**\ rticle **t**\ ext **i**\ n
**ht**\ ml documents. Check out the new twitter-bootstrap-ready
`demo <http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/bootstrapify?url=http://phys.org/news/2014-12-faster-than-light-particles.html>`__
produced by the new extraction algorithm!

Latest News
~~~~~~~~~~~

Check out my latest project: `autocomplete - a kid and adult friendly
exercise in machine
learning <https://github.com/rodricios/autocomplete>`__

I'm collaborating with `Tim Weninger <http://www3.nd.edu/~tweninge/>`__
in a must-read data-driven opinion piece (publish date is tba). I
benchmarked Eatiht and many more content extractors; you can follow the
`current work
here! <https://github.com/rodricios/crawl-to-the-future>`__.

Read `Matthew Peters's <https://github.com/matt-peters>`__ article that
benchmarked Eatiht, along with few other content extractors written in
Python.

tl;dr: Eatiht's etv2 is fast, but not so accurate (my own research
suggests that the original algo is more reliable).

Check out eatiht's `website <http://rodricios.github.io/eatiht/>`__
where I walk through each step in the original algorithm!

Follow me on `twitter <https://twitter.com/rodricios>`__ :)

What people have been saying
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*You should write a paper on this work* -
`/u/queue\_cumber <http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz0vfj>`__

*This is neat-o. A short and sweet project...* -
`/u/CandyCorns\_ <http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz17gv>`__

*This is both useful and shows a simple use case for data mining for the
general population - an outreach of sorts.* -
`/u/tweninger <http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmzai6s>`__

At a Glance
-----------

To install:
^^^^^^^^^^^

.. code:: bash

    pip install eatiht
    ...
    easy_install eatiht

Note: On Windows, you may need to install lxml manually using: pip
install lxml

Using in Python
^^^^^^^^^^^^^^^

Currently, there are two new submodules:

-  etv2.py - class-based approach

-  v2.py - script-like approach

As `requested <https://github.com/rodricios/eatiht/issues/3>`__,
etv2.extract will extract not only the text, but also the parent
element's html:

.. code:: python

    import eatiht.etv2 as etv2

    url = "http://sputniknews.com/middleeast/20141225/1016239222.html"

    tree = etv2.extract(url)

    # we know what this does...
    # print tree.get_text()

    # add necessary link tags to bootstrap cdn, center content, etc.
    tree.bootstrapify()

    print tree.get_html_string()

Output:

::

    <html><head><title>Syrian Army Kills Nearly 5,000 IS Militants in Three Months: Source / Sputnik International</title>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css" type="text/css" rel="stylesheet"></head>
    <body><h2>Syrian Army Kills Nearly 5,000 IS Militants in Three Months: Source / Sputnik International</h2>...

Now what about if that's rendered?

`With
boostrap <http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/bootstrapify?url=http://sputniknews.com/middleeast/20141225/1016239222.html>`__

`Without <http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/backto95?url=http://sputniknews.com/middleeast/20141225/1016239222.html>`__

etv2 uses classes defined in
`eatiht\_trees.py <https://github.com/rodricios/eatiht/blob/master/eatiht/eatiht_trees.py>`__
to construct what is sometimes known as the "state space" in the world
of AI. But instead of only keeping track of averages and totals - as is
required for the algorithm - the "state" class
`TextNodeSubTree <https://github.com/rodricios/eatiht/blob/master/eatiht/eatiht_trees.py#L7>`__
also keeps a reference to its original lxml.html element from whence it
came.

You can access the original, extracted html elements like this:

.. code:: python

    subtrees = tree.get_subtrees()

    first_subtree = subtrees[0]

    first_subtree.get_html()
    # <Element div at 0x2f88cc8>

    first_subtree.get_html().tag
    # 'div'

Please refer to
`eatiht\_trees.py <https://github.com/rodricios/eatiht/blob/master/eatiht/eatiht_trees.py>`__
for more info on what functions are available for you to use.

v2 is functionally identical to the original eatiht:

.. code:: python

    import eatiht.v2 as v2

    url = 'http://www.washingtonpost.com/blogs/the-switch/wp/2014/12/26/elon-musk-the-new-tesla-roadster-can-travel-some-400-miles-on-a-single-charge/'

    print v2.extract(url)

Output:

::

    Car nerds, you just got an extra present under the tree.

    Tesla announced Friday an upgrade for its Roadster, the electric car company’s convertible model,
    and said that the new features significantly boost its range -- beyond what many traditional cars
    can get on a tank of gasoline.

v2 contains one extra function that executes the extraction algorithm,
but along with returning the text, it also returns the structures that
were used to calculate the output (ie. histogram, list of xpaths, etc.):

.. code:: python

    results = v2.extract_more(url)

    results[0]      # extracted text
    results[1]      # frequency distribution (histogram)
    results[2]      # subtrees (list of textnodes pre-filter)
    results[3]      # pruned subtrees
    results[4]      # list of paragraphs (as seperated in original website)

Now whether or not this function's output looks messy is up for debate;
I personally think it looks messy and difficult to remember which index
leads to what.

I suggest using this module if you simply want the extracted text.

And of course, there is the original:

.. code:: python

    # from initial release
    import eatiht

    url = 'http://news.yahoo.com/curiosity-rover-drills-mars-rock-finds-water-122321635.html'

    print eatiht.extract(url)

Output
''''''

::

    NASA's Curiosity rover is continuing to help scientists piece together the mystery of how Mars
    lost its surface water over the course of billions of years. The rover drilled into a piece of
    Martian rock called Cumberland and found some ancient water hidden within it...

Using as a command line tool:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    eatiht http://news.yahoo.com/curiosity-rover-drills-mars-rock-finds-water-122321635.html >> out.txt

Note: Window's users may have to add the C:directory to your
`"path" <http://www.computerhope.com/issues/ch000549.htm>`__ so that the
command line tool works from any directory, not only the ..directory.

Requirements
------------

::

    lxml
    *requests, as of v0.1.0, is no longer required

Motivation
----------

After searching through the deepest crevices of the internet for some
tool\|library\|module that could effectively extract the main content
from a website (ignoring text from ads, sidebar links, etc.), I was
slightly disheartened by the apparent ambiguity caused by this
content-extraction problem.

My survey resulted in some of the following solutions:

-  `boilerpipe <https://code.google.com/p/boilerpipe/>`__ - *Boilerplate
   Removal and Fulltext Extraction from HTML pages*. Java library
   written by Christian Kohlschütter
-  `"The Easy Way to Extract Useful Text from Arbitrary
   HTML" <http://ai-depot.com/articles/the-easy-way-to-extract-useful-text-from-arbitrary-html/>`__
   - a Python tutorial on implementing a neural network for html content
   extraction. Written by alexjc
-  `Pyteaser's Cleaners
   module <https://github.com/xiaoxu193/PyTeaser/blob/master/goose/cleaners.py>`__
   - from what I can tell, it's a purely heuristic-based process
-  `"Text Extraction from the Web via Text-to-Tag
   Ratio" <http://www.cse.nd.edu/~tweninge/pubs/WH_TIR08.pdf>`__ - a
   thesis on Text-to-Tag-heuristic driven clustering as a solution for
   the problem at hand. Written by Tim Weninger & William H. Hsu

The number of research papers I found on the subject largely outweighs
the number available open-source projects. This is my attempt at
balancing out the disparity.

In the process of coming up with a solution, I made two unoriginal
observations:

1. XPath's select all (//), parent node (..) queries and functions
   ('string-length') are remarkably powerful when used together
2. Unnecessary machine learning is unnecessary

By making an assumption on sentence length, and this is trivial, one can
query for text-nodes satisfying said sentence length, then create a
frequency distribution (histogram) across the parent-nodes, and the
argmax of the resulting distribution is the xpath that is shared amongst
likely sentences.

The results were surprisingly good. I personally prefer this approach to
the others as it seems to lie somewhere in between the purely rule-based
and the drowning-in-ML approaches.

Issues or Contact
-----------------

Please raise any `issues <https://github.com/rodricios/eatiht/issues>`__
or yell at me at rodrigopala91@gmail.com or
[@rodricios](https://twitter.com/rodricios)

Tests
-----

Currently, the tests are lacking. But please still run these tests to
ensure that modifications to eatiht.py, v2.py, and etv2.py run properly.

.. code:: python

    python setup.py test

TODO:
-----

-  [STRIKEOUT:HTML-and-text extraction]
-  etv2 command line scripts
-  [STRIKEOUT:etv2.py tests]
-  improve filtering\|pruning step so that taglines from articles get
   dropped

   -  if and only if tagline has a reference image, don't prune

-  add some template engine (see "bootstrapify" function for current
   state)

