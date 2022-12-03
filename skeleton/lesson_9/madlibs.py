import random


# make a dictionary for our madlibs
words = {'nouns': ['Eric', 'panda', 'tornado', 'typhoon'],
         'adjectives': ['giant', 'angry', 'sad', 'joyful'],
         'verbs': ['eats', 'worships', 'drinks', 'attacks', 'pets'],
         'ing': ['sleeping', 'pooping', 'smiling', 'partying'],
         'adverbs': ['reluctantly', 'really', 'happily', 'quickly']}


def rand_ind(my_list: list):
    """
    Returns a random item from the provided list
    :param my_list:
        non-empty list
    :return:
        an item from the list
    """
    if len(my_list) < 1:
        return ''
    else:
        return my_list[random.randint(0, len(my_list)-1)]


def generate(my_dict: dict):
    """
    Makes a sentence given a madlibs words dictionary!

    :param my_dict:
        dict, A populated dictionary of key: list pairs with the keys "nouns", "adjectives", "verbs", "ing",
        and "adverbs".
    :return:
        None, prints a random sentence made from the dictionary
    """
    sentence = ' '.join([rand_ind(my_dict['adjectives']),
                         rand_ind(my_dict['nouns']),
                         rand_ind(my_dict['adverbs']),
                         rand_ind(my_dict['verbs']),
                         rand_ind(my_dict['ing']),
                         rand_ind(my_dict['nouns'])])
    print(sentence)

