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


def string_replace(i_string, pattern, newpattern):
    """
    Substitute specific pattern in a string by another
    :param i_string: a string
    :param pattern: the pattern of character or text which need to be substituted
    :param newpattern: replacement pattern
    :return: a string corrected
    """
    string_corrected = re.sub(pattern, newpattern, i_string)
    return string_corrected
