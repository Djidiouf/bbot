# -------------------------------------------------------------------------------
# Name:         bbot
# Purpose:      a bot without limits
#
# Author:       Djidiouf
#
# Created:      2015-07-23
# Licence:      bchat-licence
# -------------------------------------------------------------------------------

# Import socket library
import socket
# Import argument library
import argparse

# Import for displaying date and time
from datetime import datetime
# Import for timezone information
import pytz

# Import for REGEX compiler
import re


# functions ---------------------------------------------------------------------
# functions that will do the handling of the servers's data


class Message:
    def __init__(self, channel):
        self.channel = channel

    # formatting needed for every message
    def send_message(self, msg):
        ircsock.send(bytes("PRIVMSG %s :" % self.channel + msg + "\r\n", "UTF-8"))

    def hello(self):
        self.send_message("Hello!")

    def give_time(self, tz_string):  # Responds to a user that inputs "!time Continent/City"
        # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

        tz = tz_string

        if tz == 'bchat':
            tz = 'Europe/London'
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
            tz = 'Europe/Stockholm'
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
            tz = 'Australia/Sydney'
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
        else:
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)

    def give_hour_equivalence(self, string):  # Responds to an input as "!meet <Continent/City> <HH:MM>"
        # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        # /!\ currently only "utc" is working

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_string = string.partition(' ')
        tz = tuple_string[0]
        time_string = tuple_string[2]

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_time = time_string.partition(':')
        simple_hour = tuple_time[0]
        simple_minute = tuple_time[2]

        # hour and minute need to be int and not string
        hour = int(simple_hour)
        minute = int(simple_minute)

        tzinfo1 = pytz.timezone(tz)
        time_utc = datetime.now(tzinfo1)
        year = datetime.now(tzinfo1).year
        month = datetime.now(tzinfo1).month
        day = datetime.now(tzinfo1).day

        self.send_message(datetime(year, month, day, hour, minute, 0, 0, tzinfo1).strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo1)
        delta = datetime(year, month, day, hour, minute, 0, 0, tzinfo1) - time_utc
        # DEBUG self.send_message("Delta is: " + str(delta))

        tzinfo_london = pytz.timezone('Europe/London')
        time_utc = datetime.now(tzinfo_london) + delta
        self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_london)

        tzinfo_stockholm = pytz.timezone('Europe/Stockholm')
        time_utc = datetime.now(tzinfo_stockholm) + delta
        self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_stockholm)

        tzinfo_sydney = pytz.timezone('Australia/Sydney')
        time_utc = datetime.now(tzinfo_sydney) + delta
        self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_sydney)


def ping():  # Respond to server pings
    ircsock.send(bytes("PONG :Pong\n", "UTF-8"))


def join_chan(chan):  # Join channel
    ircsock.send(bytes("JOIN %s\r\n" % chan, "UTF-8"))


def regex_coder(message, expression, convention):
    p = re.compile(expression)  # Compile Regular Expression
    decoded_ircmsg = message.decode('utf-8')  # decode ircmsg to string
    string_search = p.search(decoded_ircmsg)  # search the string for RE

    if convention == 1:  # search for \r\n
        if string_search:
            msg_decoded = decoded_ircmsg[:string_search.start()]
            coded = bytes(msg_decoded, 'utf-8')
            return coded
    elif convention == 2:
        if string_search:
            msg_decoded = string_search.group()
            return msg_decoded
    elif convention == 3:  # Get Last word
        if string_search:
            msg_decoded = decoded_ircmsg[string_search.end():]
            return msg_decoded
    else:
        print("convention not found")


# arguments ---------------------------------------------------------------------
parser = argparse.ArgumentParser(description='bbot, a bot without limits')
parser.add_argument("-s", "--server", help="Server name", required=True)
parser.add_argument("-c", "--channel", help="Channel name", required=True)
parser.add_argument("-b", "--botnick", help="bbot nickname", required=True)
args = parser.parse_args()


# connection --------------------------------------------------------------------
# connect and join the configured channel
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((args.server, 6667))  # Connect to port 6667

# Sends the username, real name etc : user authentication
ircsock.send(bytes("USER %s %s %s :%s\r\n" % (args.botnick, args.botnick, args.botnick, args.botnick), "UTF-8"))

# Assignment of a nick to the bot
ircsock.send(bytes("NICK %s\r\n" % args.botnick, "UTF-8"))

# After connection, oin the specified channel
join_chan(args.channel)


# data reception ---------------------------------------------------------------
# Receive all the data from the server & channel
while 1:  # infinite loop
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip(bytes("\n\r", "UTF-8"))  # removes unnecessary linebreaks
    print(ircmsg)  # DEBUG: print output of the channel

    # tracks PING : if the server pings the bot, it will answer
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1:
        ping()

    # tracks "Hello <botname> <any message>"
    if ircmsg.find(bytes(":Hello %s" % args.botnick, "UTF-8")) != -1:
        Message(args.channel).hello()

    # tracks "!time <Continent/City>"
    if ircmsg.find(bytes(":!time", "UTF-8")) != -1:
        try:
            # time_zone = 'Australia/Sydney'
            input_string = regex_coder(ircmsg, ":!time\s", 3)
            Message(args.channel).give_time(input_string)
        except:
            Message(args.channel).send_message("Usage: !time <time_zones>")
            Message(args.channel).send_message("Purpose: Give the time in the specified time zone")
            Message(args.channel).send_message("Tip: Valid time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")

    # tracks "!meet <Continent/City> <HH:MM>"
    if ircmsg.find(bytes(":!meet", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!meet\s", 3)
            Message(args.channel).give_hour_equivalence(input_string)
        except:
            Message(args.channel).send_message("Usage: !meet utc <HH:MM>")
            Message(args.channel).send_message("Purpose: Give the equivalence of the specified utc time input in several time zones")
            Message(args.channel).send_message("Tip: Only utc time zone works at this moment")
