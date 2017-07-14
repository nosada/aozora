#!/bin/python

import argparse
import codecs
import random
import sys
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


def get_listed_text(content):
    """Return list which splited '。' for given :content:."""

    listed_text = []
    for text in content.split("。"):
        text = text.replace('\u3000', '')
        text = text.replace('\n', '')
        if not text:
            continue
        listed_text.append(text)
    return listed_text


def get_random_characters(listed_content, number):
    """Return characters from text constructed from given :listed_content:.
    length of characters are specified by given :number:."""

    text = ''.join(listed_content)
    characters = ''
    for _ in range(number):
        randomized_index = random.randint(0, len(text))
        characters += text[randomized_index]
    return characters


def get_beautifulsoup_from_html(location):
    """Return BeautifulSoup object from HTML which located to
    given :location:."""

    if "http" in location[:5]:
        try:
            file_object = urlopen(location)
            html = file_object.read()
        except (HTTPError, URLError) as caught_error:
            sys.stderr.write(caught_error)
            sys.exit(1)
    else:
        try:
            with codecs.open(location, 'r', "Shift-JIS") as file_object:
                html = file_object.read()
        except ValueError as caught_error:
            sys.stderr.write(caught_error)
            sys.exit(1)

    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"class": "main_text"}).get_text()
    return content


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description="Get random sentences from given Aozora Bunko HTML")
    PARSER.add_argument(
        "location",
        metavar="<location>",
        type=str,
        help="Location for Aozora Bunko HTML")
    PARSER.add_argument(
        "chars_number",
        metavar="<chars_number>",
        type=int,
        help="Number of sentences you want to get from given text")

    ARGS = PARSER.parse_args()
    LOCATION = ARGS.location
    CHARS_NUMBER = ARGS.chars_number

    CONTENT = get_beautifulsoup_from_html(LOCATION)
    LISTED_TEXT = get_listed_text(CONTENT)
    RANDOMIZED_CHARS = get_random_characters(LISTED_TEXT, CHARS_NUMBER)
    print(RANDOMIZED_CHARS)
