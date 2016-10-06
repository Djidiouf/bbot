__author__ = 'Djidiouf'

# Python built-in modules
from datetime import datetime  # displaying date and time
import re # REGEX compiler

# Third-party modules
import pytz  # timezone information

# Project modules
import modules.connection


def capitalize_timezone(tz_string):
    # Capitalized the tz_requested given
    tz_regex = re.compile(r"\w{1,}")
    tz_split_list = tz_regex.findall(tz_string)

    if len(tz_split_list) == 1:
        tz_split_list[0] = str.upper(tz_split_list[0])
    elif len(tz_split_list) > 1:
        for index, word in enumerate(tz_split_list):
            tz_split_list[index] = str.capitalize(word)

    tz_requested = '/'.join(tz_split_list)
    return tz_requested


def give_time(tz_string):
    """
    Responds to a user that inputs "!time <Continent/City>"
    Timezone available here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    :param tz_string: a string with these elements: "<Continent/City>"
    :print: Time in the specified timezone
    """

    tz = tz_string

    try:
        tzinfo = pytz.timezone(tz)
        time_utc = datetime.now(tzinfo)
        modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
    except pytz.exceptions.UnknownTimeZoneError:
        modules.connection.send_message("Timezone not found")
        raise ValueError('Timezone not found')


def give_hour_equivalence(i_string):
    """
    Responds to an input as "!meet <Continent/City> <HH:MM>"
    Timezone available here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    /!\ currently only "utc" is working

    :param i_string: a string with these elements: "<Continent/City> <HH:MM>"
    :print: time in different timezones
    """

    # divide a string in a tuple: 'str1', 'separator', 'str2'
    tuple_string = i_string.partition(' ')
    tz_requested = tuple_string[0]
    time_string = tuple_string[2]

    # divide a string in a tuple: 'str1', 'separator', 'str2'
    tuple_time = time_string.partition(':')
    simple_hour = tuple_time[0]
    simple_minute = tuple_time[2]

    tz_requested = capitalize_timezone(tz_requested)

    try:
        tz_requested = pytz.timezone(tz_requested)
    except pytz.exceptions.UnknownTimeZoneError:
        modules.connection.send_message("Timezone not found")
        raise ValueError('Timezone not found')

    # UTC detailed
    # time_utc = datetime.now(pytz.utc)
    # modules.connection.send_message("DEBUG UTC: " + time_utc.strftime(format))
    year_utc = datetime.now(pytz.utc).year
    month_utc = datetime.now(pytz.utc).month
    day_utc = datetime.now(pytz.utc).day
    hour_utc = datetime.now(pytz.utc).hour
    minute_utc = datetime.now(pytz.utc).minute
    hour = int(simple_hour)      # Need to be int and not string
    minute = int(simple_minute)  # Need to be int and not string

    format = "%Y-%m-%d - %H:%M:%S - %Z%z"

    # modules.connection.send_message("DEBUG req: " + str(hour) +"H : " + str(minute) + "M")
    # modules.connection.send_message("DEBUG utc: " + str(hour_utc) +"H : " + str(minute_utc) + "M")

    # hour_diff = hour - hour_utc
    # minute_diff = minute - minute_utc
    # modules.connection.send_message("DEBUG diff: " + str(hour_diff) +"H : " + str(minute_diff) + "M")

    hour_req = datetime.now(tz_requested).hour
    minute_req = datetime.now(tz_requested).minute
    decal_h = hour_req - hour_utc
    decal_m = minute_req - minute_utc
    # modules.connection.send_message("DEBUG decalageH: " + str(hour_req) + " - " + str(hour_utc) + " = " + str(decal_h))
    # modules.connection.send_message("DEBUG decalageM: " + str(minute_req) + " - " + str(minute_utc) + " = " + str(decal_m))

    hour_new = hour-decal_h
    minute_new = minute-decal_m

    # print("hour_new  : " + str(hour_new))
    # print("minute_new: " + str(minute_new))

    if hour_new < 0:
        hour_new += 24
        # print("---- hour_new +24")
    if hour_new == 24:
        hour_new = 0
    if hour_new > 24:
        hour_new -= 24
        # print("---- hour_new -24")
    if minute_new == 60:
        minute_new = 0
        hour_new += 1
        # print("---- hour_new +1")
    if minute_new > 60:
        minute_new -= 60
        hour_new += 1
        # print("---- hour_new +1")
    if minute_new < 0:
        minute_new += 60
        hour_new -= 1
        # print("---- hour_new -1")

    # print("hour_new revised: " + str(hour_new))
    # print("minute_new revis: " + str(minute_new))

    # time_requested = datetime(year_utc, month_utc, day_utc, hour_new, minute_new, 0, 0, pytz.utc).astimezone(pytz.timezone(str(tz_requested)))
    # modules.connection.send_message(time_requested.strftime(format) + " - %s" % str(tz_requested))

    tz_one = "Europe/London"
    tz_two = "Europe/Oslo"
    tz_three = "Australia/Sydney"
    time_one = datetime(year_utc, month_utc, day_utc, hour_new, minute_new, 0, 0, pytz.utc).astimezone(pytz.timezone(tz_one))
    modules.connection.send_message(time_one.strftime(format) + " - %s" % tz_one)
    time_two = datetime(year_utc, month_utc, day_utc, hour_new, minute_new, 0, 0, pytz.utc).astimezone(pytz.timezone(tz_two))
    modules.connection.send_message(time_two.strftime(format) + " - %s" % tz_two)
    time_three = datetime(year_utc, month_utc, day_utc, hour_new, minute_new, 0, 0, pytz.utc).astimezone(pytz.timezone(tz_three))
    modules.connection.send_message(time_three.strftime(format) + " - %s" % tz_three)


def main(i_string):

    # If tz_string is only 2 letters, it can be used to request time zones for a code country
    if len(i_string) == 2:
        tz = str.upper(i_string)
        if tz in pytz.country_timezones:
            modules.connection.send_message("Timezones available for " + tz + ":")
            modules.connection.send_message(', '.join(pytz.country_timezones(tz)))
            return
        else:
            modules.connection.send_message("This country code is not recognized as a valid ISO-3166 country code.")
            return

    # if tz_string is a given and recognized word, it can be used to trigger specific timezone queries
    if i_string == 'bchat':
        give_time('Europe/London')
        give_time('Europe/Oslo')
        give_time('Australia/Sydney')
    else:
        # Capitalized the tz_requested given
        tz_requested = capitalize_timezone(i_string)
        give_time(tz_requested)
