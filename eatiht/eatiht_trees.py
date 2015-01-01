"""eatiht v2 - Rodrigo Palacios - Copyright 2014"""


from lxml.html import builder as E
from lxml.html import tostring as htmltostring

class TextNodeSubTree(object):
    """ This class can be described in a few different ways. A proper
    explanation requires a brief definition of terms.

    There's two W3C-spec'd conceptual pieces that I make use of:

    TEXT_NODE - #text - NodeType 3
    ------------------
    A text node is a W3C node type. Its description is a node that
    "represents textual content in an element or attribute."

    You'll see me write this as textnode, tnode, tnd(?) in cases where
    function names get too long, or I get lazy - rarely will you get see
    me refer its named constant TEXT_NODE.

    This html element is probably the most intuitive out of all html
    elements. For one, it's always a leaf node, meaning, it's always(?)
    a last node of any branch in the html tree.

    One property of the textnode that sort of forces an intuitive, as
    opposed to explicit, acknowledgement of the textnode is that it is
    usually not visible in web dev. tools. It never dawned on me, until
    I used a python parser, that "text" in paragraph (<p>) nodes are
    actually nodes themselves!

    This diagram shows what I describe above:
    When we see this...
    ...
    <p>
        Foo
    </p>
    ...
    It means this...
    ...
    <p>
        <#text>Foo</#text>
    </p>
    ...
    Note: don't quote me about the actual #text tag representation I used.

    ELEMENT_NODE - p, div, span, etc. - NodeType 1
    The second conceptual piece that's required for this class is the
    what most people have seen out in wild.

    In the context of this algorithm/class, and many other approaches to
    text extraction, the element node is the key stone to this data
    structure.

    Without wasting too many words, as I predict you'll eventually get
    bored of these lengthy docstrings, the element node can take form of
    long list of nodes (tags), except:

        script, noscript, style, i, b, strong, span, a (this list is
        subject to additions.)

    You'll see me refer to this node as elementnode, elemnode, enode.

    Now Combining the Two - TEXT_NODE and ELEMENT_NODE
    --------------------------------------------------

    In essence, this algorithm captures the natural parent-children
    structure already present in any given html tree. The parent
    is an ELEMENT_NODE, the children are TEXT_NODES.

    In one of the first steps of the algorithm, we try to filter out,
    or prune, subtrees that have text, but exist *under* a parent elemnode
    in the above referenced list of elemnode exceptions.

    Important note about "//text()"
    -------------------------------

    consider:

    ...
    <p>
        I'm
        <b>Foo</b>
        Bar
    </p>
    ...

    reconsider this list of exception elemnodes which we "pruned":

        script, noscript, style, i, b, strong, span, a

    If you forgot what "//text()" does, it is saying, "select all textnodes"

    So after that xpath execution, you might think that we'll end up with
    only these textnodes

    [
        #text("I'm"),
        #text("Bar")
    ]

    If you don't think that, then you're good and can skip down a bit.

    If you think that that's we'll end up getting, then consider the
    following:

    In executing "//text()", your xpath query environment/engine will
    gather this list of nodes:

    [
        #text("I'm"),
        #text("Foo"),
        #text("Bar")
    ]

    And now let's add just one of the exceptions from our list of nodes
    to exceptions (please, dont confuse my use of "exceptions" with what
    we programmers know as runtime errors and exceptions) to our xpath
    query:

        //text() -----> //*[not(self::b)]//text()

    This produces, to little surprise:

    [
        #text("I'm"),
        #text("Bar")
    ]

    Wouldn't this be counterintuitive? We essentially are cutting one-third
    of our textual data.

    I unintentionally digressed to explaining the origin of the xpath. Bear
    with me. And feel free to skip this, as I think I've explained the
    intuition behind this structure enough.
    """

    # this may be a possible approach to make this class more generalized
    #def __init__(self, *args, **kwargs):
        #args -- tuple of anonymous arguments
        #kwargs -- dictionary of named arguments
        #super(TextNodeSubTree, self).__init__()
        #self.parent_path = kwargs.get('parpath')

    def __init__(self, parent_elem, parent_path, tnodes):
        """This is a structure that is explained above.
        parpath     = path to root
        tnodes      = list of children textnodes
        """
        super(TextNodeSubTree, self).__init__()
        # subtree's root element (aka wrapping html)
        self.__parent_elem = parent_elem
        # subtree parent's path
        self.__parent_path = parent_path
        # number of text children
        self.__text_nodes = tnodes
        # calculate the feature's values
        self.__learn_oneself()
        self.clean()

    def __learn_oneself(self):
        """calculate cardinality, total and average string length"""
        if not self.__parent_path or not self.__text_nodes:
            raise Exception("This error occurred because the step constructor\
                            had insufficient textnodes or it had empty string\
                            for its parent xpath")
        # Iterate through text nodes and sum up text length
        # TODO: consider naming this child_count or cardinality
        # or branch_cnt
        self.tnodes_cnt = len(self.__text_nodes)
        # consider naming this total
        self.ttl_strlen = sum([len(tnode) for tnode in self.__text_nodes])
        # consider naming this average
        self.avg_strlen = self.ttl_strlen/self.tnodes_cnt

    def get_text(self):
        """Return all joined text in textnodes"""
        return "".join(self.__text_nodes)

    def get_html(self):
        """Return the html that wraps around the text"""
        return self.__parent_elem

    def clean(self):
        """clean up newlines"""
        for textnode in self.__text_nodes:
            textnode.strip()

    @property
    def parent_path(self):
        """parent_path getter"""
        return self.__parent_path


class TextNodeTree(object):
    """collection of textnode subtrees"""
    def __init__(self, title, subtrees, hist):
        """This is a structure that is explained above."""
        super(TextNodeTree, self).__init__()
        self.__title = title
        self.__subtrees = subtrees
        self.__histogram = hist
        self.__content_path = hist[0][0]

        self.__htmltree = None
        self.__fulltext = ""

    @property
    def get_subtrees(self):
        """Return all subtrees"""
        return self.__subtrees

    @property
    def histogram(self):
        """Return frequency distribution used to find the best subtree"""
        return self.__histogram

    @property
    def title(self):
        """Return title of website"""
        return self.__title

    @property
    def content_path(self):
        """Return xpath to main content"""
        return self.__content_path

    def __make_tree(self):
        """Build a tree using lxml.html.builder and our subtrees"""

        # create div with "container" class
        div = E.DIV(E.CLASS("container"))

        # append header with title
        div.append(E.H2(self.__title))

        # next, iterate through subtrees appending each tree to div
        for subtree in self.__subtrees:
            div.append(subtree.get_html())

        # Connect div to body
        body = E.BODY(div)

        # attach body to html
        self.__htmltree = E.HTML(
            E.HEAD(
                E.TITLE(self.__title)
                ),
            body
            )

    def get_html(self):
        """Generates if need be and returns a simpler html document with text"""
        if self.__htmltree is not None:
            return self.__htmltree
        else:
            self.__make_tree()
            return self.__htmltree

    def get_html_string(self):
        """Generates if need be and returns a simpler html string with
        extracted text"""
        if self.__htmltree is not None:
            return htmltostring(self.__htmltree)
        else:
            self.__make_tree()
            return htmltostring(self.__htmltree)

    def get_text(self):
        """Return all joined text from each subtree"""
        if self.__fulltext:
            return self.__fulltext
        else:
            self.__fulltext = "\n\n".join(text.get_text()
                                          for text in self.__subtrees)
            return self.__fulltext

    # TODO: I consider this a "prototype" to the template generator
    # Clearly, bootstrap shouldn't be the only styling possible
    def bootstrapify(self):
        """Add bootstrap cdn to headers of html"""
        if self.__htmltree is None:
            #raise Exception("HtmlTree has not been made yet")
            self.__make_tree()

        # add bootstrap cdn to head
        self.__htmltree.find('head').append(
            E.LINK(rel="stylesheet",
                   href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css",
                   type="text/css"))

        # center images
        for img_parent in self.__htmltree.xpath("//img/.."):
            # the space before the class to insert is CRITICAL!
            img_parent.attrib["class"] += " text-center"

        # make images responsive
        for img in self.__htmltree.xpath("//img"):
            # the space before the class to insert is CRITICAL!
            img.attrib["class"] += " img-responsive"
