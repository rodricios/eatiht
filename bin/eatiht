#!/usr/bin/env python

import eatiht

import argparse

parser = argparse.ArgumentParser(description='A tool for extracting article text in html documents.\nSimply provide a URL, and this tool print out the main article\'s to the console.')

parser.add_argument('URL', metavar='U', type=str,
                   help='the URL to parse and extract the main article\'s text from')

args = parser.parse_args()

print eatiht.extract(args.URL)
