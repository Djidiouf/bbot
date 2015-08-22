__author__ = 'Djidiouf'

# Python built-in modules
from datetime import datetime  # displaying date and time

# Third-party modules
import pytz  # timezone information

# Project modules
import modules.connection


def give_time(tz_string):
    """
    Responds to a user that inputs "!time <Continent/City>"
    Timezone available here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    :param tz_string: a string with these elements: "<Continent/City>"
    :print: Time in the specified timezone
    """

    tz = tz_string

    if tz == 'bchat':
        tz = 'Europe/London'
        tzinfo = pytz.timezone(tz)
        time_utc = datetime.now(tzinfo)
        modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
        tz = 'Europe/Stockholm'
        tzinfo = pytz.timezone(tz)
        time_utc = datetime.now(tzinfo)
        modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
        tz = 'Australia/Sydney'
        tzinfo = pytz.timezone(tz)
        time_utc = datetime.now(tzinfo)
        modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
    else:
        try:
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
        except pytz.exceptions.UnknownTimeZoneError:
            modules.connection.send_message("Timezone not found, don't forget to capitalize it: Europe/Oslo")
            return


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
    tz = tuple_string[0]
    time_string = tuple_string[2]

    # divide a string in a tuple: 'str1', 'separator', 'str2'
    tuple_time = time_string.partition(':')
    simple_hour = tuple_time[0]
    simple_minute = tuple_time[2]

    # hour and minute need to be int and not string
    hour = int(simple_hour)
    minute = int(simple_minute)

    try:
        tzinfo1 = pytz.timezone(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        modules.connection.send_message("Timezone not found, don't forget to capitalize it: Europe/Oslo")
        return

    time_utc = datetime.now(tzinfo1)
    year = datetime.now(tzinfo1).year
    month = datetime.now(tzinfo1).month
    day = datetime.now(tzinfo1).day

    modules.connection.send_message(datetime(year, month, day, hour, minute, 0, 0, tzinfo1).strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo1)
    delta = datetime(year, month, day, hour, minute, 0, 0, tzinfo1) - time_utc
    # DEBUG modules.messages.Message(config.channel).send_message("Delta is: " + str(delta))

    tzinfo_london = pytz.timezone('Europe/London')
    time_utc = datetime.now(tzinfo_london) + delta
    modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_london)

    tzinfo_stockholm = pytz.timezone('Europe/Stockholm')
    time_utc = datetime.now(tzinfo_stockholm) + delta
    modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_stockholm)

    tzinfo_sydney = pytz.timezone('Australia/Sydney')
    time_utc = datetime.now(tzinfo_sydney) + delta
    modules.connection.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_sydney)
