__author__ = 'Djidiouf'

import re  # Regular Expression library


def string_cleanup(x, notwanted):
    for item in notwanted:
        x = re.sub(item, '', x)
    return x
