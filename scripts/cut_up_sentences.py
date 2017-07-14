#!/bin/python

import codecs
import random
import sys
import argparse
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


def get_random_sentences(listed_content, number):
    """Return characters from text constructed from given :listed_content:.
    length of characters are specified by given :number:."""

    sentences = []
    lines_of_text = len(listed_content)
    for _ in range(number):
        randomized_index = random.randint(0, lines_of_text-1)
        sentences.append(listed_content[randomized_index])
    return '\n'.join(sentences)


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
        "sentences_number",
        metavar="<sentences_number>",
        type=int,
        help="Number of sentences you want to get from given text")

    ARGS = PARSER.parse_args()
    LOCATION = ARGS.location
    SENTENCES_NUMBER = ARGS.sentences_number

    CONTENT = get_beautifulsoup_from_html(LOCATION)
    LISTED_TEXT = get_listed_text(CONTENT)
    RANDOMIZED_SENTENCES = get_random_sentences(LISTED_TEXT, SENTENCES_NUMBER)
    print(RANDOMIZED_SENTENCES)
