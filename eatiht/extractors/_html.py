"""Refactored, overhauled, and simplifying eatiht.

The reasons for these breaking changes are empirically justified (refer to
work by Weninger, Palacios, et. al."""

import urllib2

import cookielib

import _eatiht as _extract


def _etree_from_url(url):
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

    return _extract._etree_from_string(content)


def extract_text(url, normalize=True):
    """From url's html, and extract main content from website"""
    return _extract.content_from_etree(_etree_from_url(url), normalize=True)


def extract_from_string(htmlstring, normalize=True):
    """Extract main content from html string"""
    return _extract.content_from_etree(_extract._etree_from_string(htmlstring),
                                       normalize=True)
