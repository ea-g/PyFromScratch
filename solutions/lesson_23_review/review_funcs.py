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
    out = arr[0]
    curr = len(out) if type(out) is str else out
    for i in arr:
        if type(i) is str:
            if curr < len(i):
                out = i
                curr = len(i)
        else:
            if curr < i:
                out = i
                curr = i
    return out


def prob(arr: list[str | int | float], query: str | int | float) -> float:
    """
    Calculates the probability of randomly selecting a given item, `query`, given a set of items, `arr`.

    :param arr: the input set of items
    :param query: the item to randomly select
    :return: probability of randomly selecting the query item from the set, arr.
    """
    # TODO: implement the function. Hint--remember for a discrete set, relative frequency will give us probability
    overall = len(arr)
    if overall == 0:
        return 0
    freq = 0
    for i in arr:
        if i == query:
            freq += 1
    return freq/overall


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
    #  4) split the text into a list of words

    # gets the page content as a BeautifulSoup object
    page = BeautifulSoup(requests.get(url).content, "html.parser")
    par = page.find_all("p")
    all_text = ""
    for i in par:
        all_text += i.get_text(separator=" ", strip=True)
    all_text = normalize(all_text)
    return all_text.split()


def normalize(text: str) -> str:
    return re.sub(r'[^\w\s]', ' ', text.lower())


if __name__ == "__main__":
    t = "https://en.wikipedia.org/wiki/Pikachu"
    l = get_text(t)
    p = prob(l, "pikachu")
    r = prob(l, "the")
    print("pikachu:", p)
    print("the:", r)

