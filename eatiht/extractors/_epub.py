"""epub extraction submodule

Open, read, and extract text from .epub

Copyright - Rodrigo Palacios
twitter: http://twitter.com/rodricios
email: rodrigopala91@gmail.com
"""

import ebooklib

from ebooklib import epub

from lxml import html

import _eaitht as _extract

def extract_sections(filepath, normalize=True):
    """Extract content and return list of sections (book's copyright sections,
    ToC, and chapters)"""

    global BOOK
    BOOK = epub.read_epub(filepath)

    texts = []

    for elem in BOOK.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        text = _extract.content_from_etree(html.fromstring(elem.content),
                                           normalize)

        texts.append(text)

    return texts

def extract_text(filepath, normalize=True):
    """Extract section's content, and join to single string"""

    return "\n\n".join(extract_sections(filepath, normalize))
