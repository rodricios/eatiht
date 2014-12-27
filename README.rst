eatiht
======

A python package for **e**\ xtracting **a**\ rticle **t**\ ext **i**\ n
**ht**\ ml documents. Check out this
`demo <http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/filter?url=http://www.nytimes.com/2014/12/18/world/asia/us-links-north-korea-to-sony-hacking.html>`__.

12/26/14 Update
~~~~~~~~~~~~~~~

New algorithm, please skip to eatiht's `usage <#using-in-python>`__ for
details.

Please refer to the issues for notes on possible bugs, improvements,
etc.

Check out eatiht's `new website <http://rodricios.github.io/eatiht/>`__
where I walk through each step in the original algorithm! It's virtually
pain-free. New writeup will be coming soon!

What people have been saying
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*You should write a paper on this work* -
`/u/queue\_cumber <http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz0vfj>`__

*This is neat-o. A short and sweet project...* -
`/u/CandyCorns\_ <http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz17gv>`__

*From a quick glance this looks super elegant! Very neat idea!* -
`/u/worldsayshi <http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz3akt>`__

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

Currently, there are two new submodules: \* eatiht\_v2.py \* etv2.py

eatiht\_v2 is functionally identical to the original eatiht

.. code:: python

    import eatiht_v2 as eatiht

    url = 'http://www.washingtonpost.com/blogs/the-switch/wp/2014/12/26/elon-musk-the-new-tesla-roadster-can-travel-some-400-miles-on-a-single-charge/'

    print eatiht.extract(url)

Output:

::

    Car nerds, you just got an extra present under the tree.

    Tesla announced Friday an upgrade for its Roadster, the electric car company’s convertible model, and said that the new features significantly boost its range -- beyond what many traditional cars can get on a tank of gasoline.

eatiht\_v2 contains one extra function that executes the extraction
algorithm, but along with outputting the text, it outputs the structures
that were used to calculate the output (ie. histogram, list of xpaths,
etc.):

.. code:: python

    results = eatiht.extract_more(url)

    results[0]      # extracted text
    results[1]      # frequency distribution (histogram)
    results[2]      # subtrees (list of textnodes pre-filter)
    results[3]      # pruned subtrees
    results[4]      # list of paragraphs (as seperated in original website)

Now whether or not this little extra function looks messy is up to
debate - I think it looks messy and difficult to remember which index
leads to what.

So to properly encapsulate those stuctures, there are new classes that
will make accessing those properties simpler:

.. code:: python

    import etv2

    url = "..."

    tree = etv2.extract(url)

    print tree.fulltext

Output:

::

    Car nerds, you just got an extra present under the tree.

    Tesla announced Friday an upgrade for its Roadster, the electric car company’s...

There are currently no public methods, only the structures present in
the *extract\_more*:

.. code:: python

    print tree.histogram

Output:

::

    [('/html/body/div[2]/div[5]/div[1]/div[1]/div/article', 8),
     ('/html/body/div[2]/div[5]/div[1]/div[6]/div/div[2]/div[2]/div[6]', 1),
     ('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li[3]/a', 1),
     ...]

Please refer to eatiht\_trees.py for more info on what properties are
available.

As of now, a feature that should be on its way is the ability to not
only have the extracted text, but also the original, immediately
surounding html. This may help with keeping a persistant look. This is a
top priority.

And of course, there is the original:

.. code:: python

    # from initial release
    import eatiht

    url = 'http://news.yahoo.com/curiosity-rover-drills-mars-rock-finds-water-122321635.html'

    print eatiht.extract(url)

Output
''''''

::

    NASA's Curiosity rover is continuing to help scientists piece together the mystery of how Mars lost its surface water over the course of billions of years. The rover drilled into a piece of Martian rock called Cumberland and found some ancient water hidden within it...

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

    requests
    lxml

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
ensure that modifications to eatiht.py and eatiht\_v2.py run properly.

.. code:: python

    python setup.py test

TODO:
-----

-  HTML-and-text extraction
-  etv2.py tests

