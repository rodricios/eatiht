eatiht
======

A python package for **e**xtracting **a**rticle **t**ext **i**n **ht**ml documents (and .epub files).

##Breaking Changes

EPUB support added!

I've restructured the entire module. Previous conventions and methods will not work in this version of eatiht. Sorry :(

Note: I decided to drop many of the other features/extractors from versions < 0.2.0 because it was empirically shown
that those additions I've made did not improve extraction accuracy, precision. Results will be coming in a paper I'm coauthoring with a few other cool guys. This branch in a way is "going back to its roots".

###What people have been saying

*You should write a paper on this work* - [/u/queue_cumber](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz0vfj)

*This is neat-o. A short and sweet project...* - [/u/CandyCorns_](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmz17gv)

*This is both useful and shows a simple use case for data mining for the general population - an outreach of sorts.* - [/u/tweninger](http://www.reddit.com/r/compsci/comments/2ppyot/just_made_what_i_consider_my_first_algorithm_it/cmzai6s)

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

#####HTML

```python
from eatiht import extract

nytimes_iran_url = "http://www.nytimes.com/2015/04/04/world/middleeast/iran-nuclear-deal.html"

nytimes_iran_story = extract.text_from_html(nytimes_iran_url)

print(nytimes_iran_story)
```

Output:

```text
TEHRAN — As word made its way around the globe that an understanding had
been reached with the United States and other powers to limit Iran’s nuclear
program, Iranians themselves greeted the news with optimism and skepticism
on Friday. While the political climate remained uncertain, the government was
allowed to promote the deal at Friday Prayer, a sign that the plan was broadly
supported by Iran’s establishment.
```

#####EPUB

Shout out to the maintainers of [ebooklib](https://github.com/aerkalov/ebooklib)  :)

```python
from eatiht import extract

sorcerersstone_path = "c:/Path/to/totally/legal/downloads/Harry Potter and the Sorcerer's Stone - J. K. Rowling.epub"

#Unfortunately, there is no "smart" algorithm that will ignore the coverpage, titlepage, copyright page(s) yet.
#Suggestions welcomed :)
sorcerersstone_sections = extract.sections_from_epub(sorcerersstone_path, normalize=False)
#set "normalize" to false if you'd like to keep the original XML-based-document's format/layout

 print(sorcerersstone_sections[4]) #the 5th section is where this book's story begins
```

Output:
```
 Chapter 1

     The Boy Who Lived

     Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that
     they were perfectly normal, thank you very much. They were the last
     people you’d expect to be involved in anything strange or mysterious,
     because they just didn’t hold with such nonsense.
     [...]
```

#####Missing Features

1. CLI
2. Title-extraction is initself a content-extraction problem to solve (this module extracts the article)
3. Lots of other stuff that you may have liked from the master branch


Note: Window's users may have to add the C:\PythonXX\Scripts directory to your ["path"](http://www.computerhope.com/issues/ch000549.htm) so that the command line tool works from any directory, not only the ..\Scripts directory.

Requirements
------------
```
lxml, chardet, ebooklib
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

Tests
-----
Currently, the tests are lacking. But please still run these tests to ensure that
modifications to eatiht.py, v2.py, and etv2.py run properly.
```python
python setup.py test
```

TODO:
-----

TODO
