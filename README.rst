eatiht
======

A python package for **e**\ xtracting **a**\ rticle **t**\ ext **i**\ n
**ht**\ ml documents. Check out this
`demo <http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/filter?url=http://www.nytimes.com/2014/12/18/world/asia/us-links-north-korea-to-sony-hacking.html>`__.

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

.. code:: python

    import eatiht 

    url = 'http://news.yahoo.com/curiosity-rover-drills-mars-rock-finds-water-122321635.html'

    print eatiht.extract(url)

Output
''''''

::

    NASA's Curiosity rover is continuing to help scientists piece together the mystery of how Mars lost its
    surface water over the course of billions of years. The rover drilled into a piece of Martian rock called
    Cumberland and found some ancient water hidden within it. Researchers were then able to test a key ratio 
    in the water with Curiosity's onboard instruments... 

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

Please raise any issues or yell at me at rodrigopala91@gmail.com or
[@mi\_ogirdor](https://twitter.com/mi\_ogirdor)
