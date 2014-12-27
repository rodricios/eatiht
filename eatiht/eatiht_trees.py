"""eatiht v2 - Rodrigo Palacios - Copyright 2014"""


from lxml.builder import E


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

    def __init__(self, parpath, tnodes):
        """This is a structure that is explained above.
        parpath     = path to root
        tnodes      = list of children textnodes
        """
        super(TextNodeSubTree, self).__init__()
        # subtree parent's path
        self.__parent_path = parpath
        # number of text children
        self.text_nodes = tnodes
        self.__learn_oneself()
        self.clean()

    def __learn_oneself(self):
        """calculate cardinality, total and average string length"""
        if not self.__parent_path or not self.text_nodes:
            raise Exception("This should never happen.")
        # Iterate through text nodes and sum up text length

        # consider naming this child_count or cardinality
        self.tnodes_cnt = len(self.text_nodes)
        # consider naming this total
        self.ttl_strlen = sum([len(tnode) for tnode in self.text_nodes])
        # consider naming this average
        self.avg_strlen = self.ttl_strlen/self.tnodes_cnt

    def clean(self):
        """clean up newlines"""
        for textnode in self.text_nodes:
            textnode.strip()

    @property
    def parent_path(self):
        """parent_path getter"""
        return self.__parent_path


class TextNodeTree(object):
    """collection of textnode subtrees"""

    def __init__(self, subtrees, subtree_texts, fulltext, hist):
        """This is a structure that is explained above."""
        super(TextNodeTree, self).__init__()
        self.subtrees = subtrees
        self.subtree_texts = subtree_texts
        self.fulltext = fulltext
        self.histogram = hist
