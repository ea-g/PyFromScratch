"""
Review usages for basic data types, relative frequency/probability
"""
import re
import requests
from bs4 import BeautifulSoup


def largest(arr: list[str | int | float]) -> str | int | float:
    """
    Looks through a list and returns the largest item. If the list contains strings, uses the length of the string as
    its size.

    :param arr: a list containing any mix of strings, ints, or floats
    :return: the largest item in the list
    """
    # TODO: Implement the function.
    pass


def prob(arr: list[str | int | float], query: str | int | float) -> float:
    """
    Calculates the probability of randomly selecting a given item, `query`, given a set of items, `arr`.

    :param arr: the input set of items
    :param query: the item to randomly select
    :return: probability of randomly selecting the query item from the set, arr.
    """
    # TODO: implement the function. Hint--remember for a discrete set, relative frequency will give us probability
    pass


def get_text(url: str) -> list[str]:
    """
    Retrieves all text from paragraph elements from a given url, normalizes it, then splits it into a list of individual
    words.

    :param url: the target webpage
    :return: a list of words from the paragraphs on the webpage
    """
    # TODO:
    #  1) get all the the paragraph elements
    #  2) extract the text from the paragraph elements and make a giant string, all_text
    #  3) normalize the text using the normalize() function (already made)
    #  4) split the text into a list

    # gets the page content as a BeautifulSoup object
    page = BeautifulSoup(requests.get(url).content, "html.parser")

    all_text = None
    pass


def normalize(text: str) -> str:
    return re.sub(r'[^\w\s]', ' ', text.lower())





