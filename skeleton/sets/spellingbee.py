from collections import defaultdict
import json
from os import PathLike
from typing import DefaultDict, Set, FrozenSet, Literal
import requests
from itertools import combinations
import fire
# import aiohttp
# import asyncio
# import sys


# TODO: make a function to validate the word using the dictionary api
# https://api.dictionaryapi.dev/api/v2/entries/en/WORDHERE
# or https://en.wiktionary.org/api/rest_v1/page/definition/WORD HERE?redirect=false


def validate_word(word: str, api: Literal["wiki", "dictionaryapi"] = "wiki") -> bool:
    # returns true if word valid (in dictionary), false otherwise
    # we'll only validate on demand--not the whole vocab since that may hit rate limits
    if api == "wiki":
        prefix = "https://en.wiktionary.org/api/rest_v1/page/definition/"
        suffix = "?redirect=false"
        raise NotImplementedError("Wikitionary not implemented! Use dictionaryapi")
    elif api == "dictionaryapi":
        prefix = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        suffix = ""
    else:
        raise ValueError(f'{api} given as api, must be "wiki" or "dictionaryapi"')
    try:
        response = requests.get(prefix + word + suffix, timeout=3)
        # TODO do something here!
        return response.status_code == 200
            

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404, 500 errors

    except requests.exceptions.ConnectionError as conn_err:
        print(
            f"Connection error occurred: {conn_err}"
        )  # DNS failure, refused connection, etc.

    except requests.exceptions.Timeout as timeout_err:
        print(f"Request timed out: {timeout_err}")  # Server took too long to respond

    except requests.exceptions.RequestException as req_err:
        # Base exception for all other request-related errors
        print(f"An error occurred: {req_err}")


def sets_to_words(words_json_fp: str | PathLike) -> DefaultDict[FrozenSet, Set]:
    # TODO: make a function to take a word, convert it to a set, add the set to the set dict if cardinality <= 7 and not present, add word to the values
    # exclude words with less than 4 letters
    out = defaultdict(set)

    # load the json
    with open(words_json_fp, "rb") as f:
        words = json.load(f)

    # put your code here, start with a for loop over the words dictionary
    for w in words:
        if len(w) >= 4:
            fz = frozenset(w)
            if len(fz) <= 7:
                out[fz].add(w)
    return out


def get_answers(letters: str, key_letter: str, vocab: DefaultDict[FrozenSet, Set]):
    # get all the subsets that have:
    # 1. the key letter
    # 2. have cardinality >= 2
    start = set(letters)
    possible_sets = list()
    # get all possible combinations of letters in the 
    for i in range(2, len(letters)+1):
        possible_sets += list(combinations(start, i))
    # convert the tuples to frozensets
    for i in range(len(possible_sets)):
        possible_sets[i] = frozenset(possible_sets[i])
    sets_to_check = list()
    # checking if the key letter is present in the possible sets
    for s in possible_sets:
        if key_letter in s:
            # if key letter is there, keep the set (add to sets_to_check)
            sets_to_check.append(s)
    answers = set()
    for s in sets_to_check:
        answers = answers | vocab[s]
    return answers

def order_answers(answers: list):
    # order so that words of the same starting letter are together and ordered by descending length (longest -> shortest)
    return sorted(answers, key = lambda x: (x, -len(x))) # TODO: fix me!

def pretty_print(answers: list):
    # print words of same length on same line with headers for each letter section
    
    # initialize
    key_letter = answers[0][0]
    header = f"=====================\nAnswers for letter {key_letter}:\n====================="
    word_len = len(answers[0])
    ln = ""
    print(header)
    for w in answers:
        if w[0] != key_letter:
            # TODO: fill me in, what to do when the first letter changes?
            header = f"\n=====================\nAnswers for letter {key_letter}:\n====================="
            # print new header
            print(header)
        if word_len != len(w):
            # TODO: fill me in, what to do when the word length changes?
            pass
        # add 
        ln = ln + w + ", "
        
            
def main(letters: str, key: str):
    # TODO: put it all together in the right order
    # optionally, make the panagrams (words that use all letters) print first 
    pass

# running async for many words at once
# if sys.platform == 'win32':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# async def fetch_word(session, word):
#     url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
#     try:
#         async with session.get(url) as response:
#             data = await response.json()
#             if isinstance(data, list):
#                 return word
#     except Exception as e:
#         print(f"Error fetching '{word}': {e}")

# async def main(words):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch_word(session, word) for word in words]
#         z = await asyncio.gather(*tasks)
#         print(z)

if __name__ == "__main__":
    words_list = ["apple", "banana", "orange", "nerfner"]
    # vocab = sets_to_words("./skeleton/sets/words_dictionary.json")
    vocab = sets_to_words("./words_dictionary.json")
    print(vocab[frozenset("taxability")])
    out = order_answers(get_answers("endivgh", "v", vocab))
    print(f"apple is valid: {validate_word('apple', api='dictionaryapi')}")
    print(f"aewsfawef is valid: {validate_word('aewsfawef', api='dictionaryapi')}")
    # asyncio.run(main(words_list))
    
    # when ready remove parts above and uncomment line below
    # fire.Fire(main)
