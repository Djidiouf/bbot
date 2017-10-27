__author__ = 'Djidiouf'

# Python built-in modules
from datetime import datetime, timedelta  # displaying date and time

# Third-party modules
import pytz  # install module: pytz  # timezone information

# Project modules
import modules.connection
import modules.time


def main(i_string, i_medium, i_alias=None):
    """
    Responds to an input as "!meet <Continent/City> <HH:MM>"
    Timezone available here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    /!\ currently only "utc" is working

    :param i_string: a string with these elements: "<Continent/City> <HH:MM>"
    :print: time in different timezones
    """

    # Divide a string in a tuple: 'str1', 'separator', 'str2'
    tuple_string = i_string.partition(' ')

    if ':' in tuple_string[0]:  # Process either !meet Europe/Oslo 10:00 or !meet 10:00 Europe/Oslo
        time_string = tuple_string[0]
        tz_requested = tuple_string[2]
    else:
        time_string = tuple_string[2]
        tz_requested = tuple_string[0]

    # Divide a string in a tuple: 'str1', 'separator', 'str2'
    tuple_time = time_string.partition(':')
    simple_hour = tuple_time[0]
    simple_minute = tuple_time[2]

    tz_requested = modules.time.capitalize_timezone(tz_requested)

    try:
        tz_requested = pytz.timezone(tz_requested)
    except pytz.exceptions.UnknownTimeZoneError:
        modules.connection.send_message("Timezone not found", i_medium, i_alias)
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

    format = "%H:%M"
    # format = "%Y-%m-%d - %H:%M:%S - %Z%z"  # full format

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
    modules.connection.send_message(time_one.strftime(format) + " - %s" % tz_one, i_medium, i_alias)
    time_two = datetime(year_utc, month_utc, day_utc, hour_new, minute_new, 0, 0, pytz.utc).astimezone(pytz.timezone(tz_two))
    modules.connection.send_message(time_two.strftime(format) + " - %s" % tz_two, i_medium, i_alias)
    time_three = datetime(year_utc, month_utc, day_utc, hour_new, minute_new, 0, 0, pytz.utc).astimezone(pytz.timezone(tz_three))
    modules.connection.send_message(time_three.strftime(format) + " - %s" % tz_three, i_medium, i_alias)
