__author__ = 'Djidiouf'

import re  # Regular Expression library


def string_cleanup(x, notwanted):
    """
    Substitute specific elements in a string by nothing
    :param x: a string
    :param notwanted: a list of elements which will be substitute
    :return: a string without these elements
    """
    for item in notwanted:
        x = re.sub(item, '', x)
    return x
