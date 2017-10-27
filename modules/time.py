__author__ = 'Djidiouf'

# Python built-in modules
from datetime import datetime, timedelta  # displaying date and time
import re # REGEX compiler

# Third-party modules
import pytz  # install module: pytz  # timezone information

# Project modules
import modules.connection


def capitalize_timezone(tz_string):
    # Capitalized the tz_requested given
    tz_regex = re.compile(r"\w{1,}")
    tz_split_list = tz_regex.findall(tz_string)
    # tz_split_list = re.split('\s|/', tz_string)

    if len(tz_split_list) == 1:                                 # Iran, Zulu, UTC, GMT...
        if len(tz_split_list[0]) > 3:                           # Iran, Zulu...
            tz_split_list[0] = str.title(tz_split_list[0])
        else:                                                   # UTC, GMT...
            tz_split_list[0] = str.upper(tz_split_list[0])
    elif len(tz_split_list) > 1:                                # America/New_York, Europe/Oslo...
        for index, word in enumerate(tz_split_list):
            tz_split_list[index] = str.title(word)

    tz_requested = '/'.join(tz_split_list)
    return tz_requested


def give_time(tz_string, i_delta=None):
    """
    Responds to a user that inputs "!time <Continent/City>"
    Timezone available here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    :param tz_string: a string with these elements: "<Continent/City>"
    :print: Time in the specified timezone
    """

    tz = tz_string
    format = "%H:%M"
    # format = "%Y-%m-%d - %H:%M:%S - %Z%z"  # full format

    try:
        tzinfo = pytz.timezone(tz)
        time_utc = datetime.now(tzinfo)
        if i_delta:
            i_delta_sign = ""
            if i_delta >= 0:
                i_delta_sign = "+"
            time_utc = time_utc + timedelta(hours=i_delta)
            results = time_utc.strftime(format) + " - %s %s%s" % (tz, i_delta_sign, i_delta)
            return results
        else:
            results = time_utc.strftime(format) + " - %s" % tz
            return results
    except pytz.exceptions.UnknownTimeZoneError:
        # modules.connection.send_message("Timezone not found")
        raise ValueError('Timezone not found')


def main(i_string, i_medium, i_alias=None):

    # If tz_string is only 2 letters, it can be used to request time zones for a code country
    if len(i_string) == 2:
        tz = str.upper(i_string)
        if tz in pytz.country_timezones:
            tz_matching = pytz.country_timezones(tz)
            if len(tz_matching) > 1:  # If there is more than 1 tz possible, list them, if not, process the tz
                modules.connection.send_message("Timezones available for " + tz + ":", i_medium, i_alias)
                modules.connection.send_message(', '.join(pytz.country_timezones(tz)), i_medium, i_alias)
            else:
                results = give_time(tz_matching[0])
                modules.connection.send_message(results, i_medium, i_alias)
            return
        else:
            modules.connection.send_message("This country code is not recognized as a valid ISO-3166 country code.", i_medium, i_alias)
            return

    utc_searched = re.search("(.*)(\+|-)(.*)", i_string, re.IGNORECASE)


    # if tz_string is a given and recognized word, it can be used to trigger specific timezone queries
    if i_string == 'bchat':
        results = give_time('Europe/London')
        modules.connection.send_message(results, i_medium, i_alias)
        results = give_time('Europe/Oslo')
        modules.connection.send_message(results, i_medium, i_alias)
        results = give_time('Australia/Sydney')
        modules.connection.send_message(results, i_medium, i_alias)
    elif utc_searched:
        tz_requested = capitalize_timezone(utc_searched.group(1))
        delta = str(utc_searched.group(2) + utc_searched.group(3))
        results = give_time(tz_requested, int(delta))
        modules.connection.send_message(results, i_medium, i_alias)
    else:
        # Capitalized the tz_requested given
        tz_requested = capitalize_timezone(i_string)
        results = give_time(tz_requested)
        modules.connection.send_message(results, i_medium, i_alias)
