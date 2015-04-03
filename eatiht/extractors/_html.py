"""Refactored, overhauled, and simplifying eatiht.

The reasons for these breaking changes are empirically justified (refer to
work by Weninger, Palacios, et. al."""

import urllib2

import cookielib

import _eatiht as _extract

from lxml.html.clean import clean_html


def _etree_from_url(url, clean=False):
    """Given URL, construct and return an element tree.
    """
    handler = (urllib2.HTTPSHandler
               if url.lower().startswith('https')
               else urllib2.HTTPHandler)

    cookiejar = cookielib.CookieJar()

    opener = urllib2.build_opener(handler)

    opener.add_handler(urllib2.HTTPCookieProcessor(cookiejar))

    resp = opener.open(url)

    try:
        content = resp.read()
    finally:
        resp.close()

    if clean:
        content = clean_html(content)

    return _extract._etree_from_string(content)


def extract_text(url, normalize=True, clean=False):
    """From url's html, and extract main content from website"""

    global HTML_ETREE
    HTML_ETREE = etree = _etree_from_url(url, clean)

    return _extract.content_from_etree(etree, normalize)


def extract_from_string(htmlstring, normalize=True, clean=False):
    """Extract main content from html string"""

    if clean:
        htmlstring = clean_html(htmlstring)

    global HTML_ETREE
    HTML_ETREE = etree = _extract._etree_from_string(htmlstring)

    return _extract.content_from_etree(etree, normalize)
