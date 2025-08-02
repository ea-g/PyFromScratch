from collections import defaultdict
import json
from os import PathLike
from typing import DefaultDict, Set, FrozenSet, Literal
import requests
import aiohttp
import asyncio

import sys




# TODO: make a function to validate the word using the dictionary api
# https://api.dictionaryapi.dev/api/v2/entries/en/WORDHERE
# or https://en.wiktionary.org/api/rest_v1/page/definition/WORD HERE?redirect=false


def validate_word(word: str, api: Literal["wiki", "dictionaryapi"] = "wiki") -> bool:
    # returns true if word valid (in dictionary), false otherwise
    # we'll only validate on demand--not the whole vocab since that may hit rate limits
    if api == "wiki":
        prefix = "https://en.wiktionary.org/api/rest_v1/page/definition/"
        suffix = "?redirect=false"
    elif api == "dictionaryapi":
        prefix = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        suffix = ""
    else:
        raise ValueError(f'{api} given as api, must be "wiki" or "dictionaryapi"')
    try:
        response = requests.get(prefix+'some'+suffix, timeout=3)

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # e.g., 404, 500 errors

    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')  # DNS failure, refused connection, etc.

    except requests.exceptions.Timeout as timeout_err:
        print(f'Request timed out: {timeout_err}')  # Server took too long to respond

    except requests.exceptions.RequestException as req_err:
        # Base exception for all other request-related errors
        print(f'An error occurred: {req_err}')
        


def sets_to_words(words_json_fp: str | PathLike) -> DefaultDict[FrozenSet, Set]:
    #     make a function to take a word, convert it to a set, add the set to the set dict if cardinality <= 7 and not present, add word to the values
    #      exclude words with less than 4 letters
    out = defaultdict(set)
    
    # load the json
    with open(words_json_fp, "rb") as f:
        words = json.load(f)
    
    # put your code here
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
    words_list = ['apple', 'banana', 'orange', 'nerfner']
    # asyncio.run(main(words_list))
