eatiht
======

A python package for **e**xtracting **a**rticle **t**ext **i**n **ht**ml documents. Check out this [demo](http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/filter?url=http://www.nytimes.com/2014/12/18/world/asia/us-links-north-korea-to-sony-hacking.html).

###12/24/14 Update

tl;dr

new and improved algorithm coming really soon (like, probably tomorrow)!

I just finished coding up an improved algorithm (v2) that makes use of a statistical property that everyone knows like the back their hand. 

The failures of the original algorithm is present in the [demo, dohh!](http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/filter?url=http://www.nytimes.com/2014/12/18/world/asia/us-links-north-korea-to-sony-hacking.html). The line that starts with,

    The administration's sudden urgency came after a new threat...

finishes way too early. The fix is explained in the next line. 

v2 does away with regex splitting - and that was likely a cause of many people's headaches, if they've been able to notice them. Due to the generally infrequent use of [?,',",!] as sentence-finishers in large texts, as opposed to plain old ".",  some of you may have not noticed. 

The bug arose on this line of [code](https://github.com/rodricios/eatiht/blob/master/eatiht/eatiht.py#L154) and caused more false-positives than anyone would like - most likely due to different encodings as @rcarmo warns about [here](https://github.com/rodricios/eatiht/issues/2). 

I'd also like to give a plug to @rcarmo's [hy port/improvement of eatiht v1](https://gist.github.com/rcarmo/bb0310c71d6573b3919c) minus the scary list-comprehensions and the regex-splitting present in the original implementation. 

There's a conversation between myself and @voidfiles [here](https://github.com/rodricios/eatiht/issues/3), and I'd like more input from concerned users. It's about whether or not this module should be constructed in an object-oriented manner (aka. use 'class'). I personally favor a side-by-side script-and-class approach, and you can read about why in the above referenced link. You, I, and @voidfiles will probably like an OO implementation because it will likely lead to plug-and-play extensions and more!

Finally, I'd like to say thanks to everyone who's tried out this module. Double thanks if you read thru the [writeup](http://rodricios.github.io/eatiht/). Double that if you showed this to your friends or coworkers. x6 if you also brought up any [issues](https://github.com/rodricios/eatiht/issues). Any of those things definitely helps one's motivation to come up with neat little solutions such as eatiht :)

Best wishes and happy holidays,

@rodricios

---

Check out eatiht's [new website](http://rodricios.github.io/eatiht/) where I walk through each step in the algorithm! It's virtually pain-free.


###What people have been saying

*You should write a paper on this work* - [/u/queue_cumber](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz0vfj)

*This is neat-o. A short and sweet project...* - [/u/CandyCorns_](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz17gv)

*From a quick glance this looks super elegant! Very neat idea!* - [/u/worldsayshi](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz3akt)

At a Glance
-----------

#### To install:

```bash
pip install eatiht
...
easy_install eatiht
```

Note: On Windows, you may need to install lxml manually using:
pip install lxml

#### Using in Python
```python
import eatiht

url = 'http://news.yahoo.com/curiosity-rover-drills-mars-rock-finds-water-122321635.html'

print eatiht.extract(url)
```
##### Output
```
NASA's Curiosity rover is continuing to help scientists piece together the mystery of how Mars lost its
surface water over the course of billions of years. The rover drilled into a piece of Martian rock called
Cumberland and found some ancient water hidden within it. Researchers were then able to test a key ratio
in the water with Curiosity's onboard instruments...
```


#### Using as a command line tool:
```bash
eatiht http://news.yahoo.com/curiosity-rover-drills-mars-rock-finds-water-122321635.html >> out.txt
```

Note: Window's users may have to add the C:\PythonXX\Scripts directory to your ["path"](http://www.computerhope.com/issues/ch000549.htm) so that the command line tool works from any directory, not only the ..\Scripts directory.

Requirements
------------
```
requests
lxml
```

Motivation
----------

After searching through the deepest crevices of the internet for some tool|library|module that could effectively extract the main content from a website (ignoring text from ads, sidebar links, etc.), I was slightly disheartened by the apparent ambiguity caused by this content-extraction problem.

My survey resulted in some of the following solutions:

* [boilerpipe](https://code.google.com/p/boilerpipe/) - *Boilerplate Removal and Fulltext Extraction from HTML pages*. Java library written by Christian Kohlschütter
* ["The Easy Way to Extract Useful Text from Arbitrary HTML"](http://ai-depot.com/articles/the-easy-way-to-extract-useful-text-from-arbitrary-html/) - a Python tutorial on implementing a neural network for html content extraction. Written by alexjc
* [Pyteaser's Cleaners module](https://github.com/xiaoxu193/PyTeaser/blob/master/goose/cleaners.py) - from what I can tell, it's a purely heuristic-based process
* ["Text Extraction from the Web via Text-to-Tag Ratio"](http://www.cse.nd.edu/~tweninge/pubs/WH_TIR08.pdf) - a thesis on Text-to-Tag-heuristic driven clustering as a solution for the problem at hand. Written by Tim Weninger & William H. Hsu

The number of research papers I found on the subject largely outweighs the number available open-source projects. This is my attempt at balancing out the disparity.

In the process of coming up with a solution, I made two unoriginal observations:

1. XPath's select all (//), parent node (..) queries and functions ('string-length') are remarkably powerful when used together
2. Unnecessary machine learning is unnecessary

By making an assumption on sentence length, and this is trivial, one can query for text-nodes satisfying said sentence length, then create a frequency distribution (histogram) across the parent-nodes, and the argmax of the resulting distribution is the xpath that is shared amongst likely sentences.

The results were surprisingly good. I personally prefer this approach to the others as it seems to lie somewhere in between the purely rule-based and the drowning-in-ML approaches.

Issues or Contact
-----------------

Please raise any [issues](https://github.com/rodricios/eatiht/issues) or yell at me at rodrigopala91@gmail.com or [@rodricios](https://twitter.com/rodricios)

TODO:
-----

* ~~Add newline and tab options for printing.~~ Please check out the [demo](http://web-tier-load-balancer-1502628209.us-west-2.elb.amazonaws.com/filter?url=http://www.nytimes.com/2014/12/18/world/asia/us-links-north-korea-to-sony-hacking.html) for the new **default** output (sorry, no options for formatting as of yet).
