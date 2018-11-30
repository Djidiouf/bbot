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
        if item.startswith("$"):
            item = "\\" + item

        x = re.sub(item, '', x)
    return x


def string_cleanup_simple(x, notwanted):
    """
    Substitute specific elements in a string by nothing
    :param x: a string
    :param notwanted: a list of elements which will be substitute
    :return: a string without these elements
    """
    for item in notwanted:
        x = x.replace(item, '')
    return x


def list_to_string(i_list):
    list_as_string = str(i_list)[1:-1]
    list_as_string = string_replace(list_as_string, "', '", " ")
    list_as_string = string_replace(list_as_string, "'), ('", ", ")
    list_as_string = string_replace(list_as_string, "('", "")
    list_as_string = string_replace(list_as_string, "')", "")
    return list_as_string


def string_replace(i_string, i_pattern, newpattern):
    """
    Substitute specific pattern in a string by another
    :param i_string: a string
    :param pattern: the pattern of character or text which need to be substituted
    :param newpattern: replacement pattern
    :return: a string corrected
    """
    #pattern = re.escape(pattern)
    #string_corrected = re.sub(pattern, newpattern, i_string)
    #return string_corrected
    string_corrected = i_string

    for pattern in i_pattern:
        pattern = re.escape(pattern)
        string_corrected = re.sub(pattern, newpattern, string_corrected)

    return string_corrected


def string_split(i_string, *delimiters):
    """
    :return: a list of string without specific delimiters
    """
    pattern = '|'.join(map(re.escape, delimiters))
    return re.split(pattern, i_string)


def chunk_string(string, length):
    """
    String split after given length
    :param string: a string
    :param length: maximum char allowed by chunk of string
    :return: a generator for all chunks of the string
    """
    return (string[0+i:length+i] for i in range(0, len(string), length))


def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False
