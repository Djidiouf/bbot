# -------------------------------------------------------------------------------
# Name:         bbot
# Purpose:      a bot without limits
#
# Author:       Djidiouf
#
# Created:      2015-07-23
# Licence:      bchat-licence
# -------------------------------------------------------------------------------

# Python built-in modules
# import argparse  # Add the possibility to have command line arguments
# # # arguments ---------------------------------------------------------------------
# # -s <server>  -c "<channel>" -b <bot nickname>
# parser = argparse.ArgumentParser(description='bbot, a bot without limits')
# parser.add_argument("-s", "--server", help="Server name", required=True)
# parser.add_argument("-c", "--channel", help="Channel name", required=True)
# parser.add_argument("-b", "--botnick", help="bbot nickname", required=True)
# args = parser.parse_args()
import configparser
import re  # REGEX compiler
import sys  # system library
import os

# Project modules
import modules.steam  # Contains specific Steam-Valve related functions
import modules.money
import modules.time
import modules.speak
import modules.connection
import modules.help
import modules.imdb


# conf = configparser.RawConfigParser()
# conf.add_section('bot_configuration')
# conf.set('bot_configuration', 'server', args.server)
# conf.set('bot_configuration', 'channel', args.channel)
# conf.set('bot_configuration', 'botnick', args.botnick)

# # Writing our configuration file to 'example.cfg'
# with open('config.cfg', 'w') as configfile:
#     conf.write(configfile)

# Read config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))  # Absolute path is better
server = config['bot_configuration']['server']
channel = config['bot_configuration']['channel']
botnick = config['bot_configuration']['botnick']
# admins_list = config.get('bot_configuration', 'admin')
admins_list = config['bot_configuration']['admins'].split(",")

# ip_format = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # IP check
ip_format = r"([^\s]+)"  # Thx to IRC specifications >:(
user_message = r"(.*)!~(.*)" + r"@" + ip_format                                 # Match: User!~User@123.123.123.123
# admin_message = re.escape(admin) + r"!~" + re.escape(admin) + r"@" + ip_format  # Match: Admin!~Admin@123.123.123.123

# REGEX ###############
# !help
help_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!help"
help_regex = bytes(help_regex, "UTF-8")

# !imdb
imdb_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!imdb"
imdb_regex = bytes(imdb_regex, "UTF-8")

# !meet
meet_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!meet"
meet_regex = bytes(meet_regex, "UTF-8")

# !money
money_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!money"
money_regex = bytes(money_regex, "UTF-8")

# !op
op_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!op"
op_regex = bytes(op_regex, "UTF-8")

# !quit
quit_user_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!quit"
quit_user_regex = bytes(quit_user_regex, "UTF-8")

# !say
say_regex = user_message + r" PRIVMSG " + re.escape(botnick) + r" :" + r"!say"
say_regex = bytes(say_regex, "UTF-8")

# !say (In private: /msg botnick !say)
say_private_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!say"
say_private_regex = bytes(say_private_regex, "UTF-8")

# !steamprice
steamprice_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!steamprice"
steamprice_regex = bytes(steamprice_regex, "UTF-8")

# !time
time_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!time"
time_regex = bytes(time_regex, "UTF-8")


def regex_coder(message, expression, convention):
    """
    Use with:
    input_string = regex_coder(ircmsg, ":!meet\s", 3)

    :param message:
    :param expression:
    :param convention:
    :return:
    """
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


def regex_search_arguments(message, expression):
    decoded_ircmsg = message.decode('utf-8')  # decode ircmsg to string
    arguments_regex = r'(?<=' + re.escape(expression) + r' )(.*)'
    string_searched = re.search(arguments_regex, decoded_ircmsg, re.IGNORECASE)
    # print("string_searched =", string_searched)  # DEBUG: <_sre.SRE_Match object; span=(65, 75), match='15 EUR:AUD'>
    arguments = string_searched.group(0)
    return arguments


def is_message_from_admin(message):
    is_from_admin = False

    decoded_ircmsg = message.decode('utf-8')  # decode ircmsg to string

    for element in admins_list:
        print("element is :", element)
        user_involved_regex = re.escape(element) + r'(?=!~' + re.escape(element) + r'@)'
        print("user_involved_regex is :", user_involved_regex)

        try:
            user_involved_searched = re.search(user_involved_regex, decoded_ircmsg, re.IGNORECASE)
            print("user_involved_searched is :", user_involved_searched)
            user_involved = user_involved_searched.group(0)
            print("user_involved is :", user_involved)
            is_from_admin = True
            break
        except AttributeError:
            is_from_admin = False
            pass

    print("is_from_admin is :", is_from_admin)
    return is_from_admin


# connect and join the configured channel
modules.connection.join_chan(channel)

# data reception ---------------------------------------------------------------
# Receive all the data from the server & channel
while 1:  # infinite loop
    ircmsg = modules.connection.receive_data()  # Receive data from the server
    ircmsg = ircmsg.strip(bytes("\n\r", "UTF-8"))  # Remove linebreaks which appear on each message
    print(ircmsg)  # DEBUG: print output of the channel

    # TRACKS ##################################################################
    # PING : if the server pings the bot, it will answer
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1:
        modules.connection.ping()

    # Hello <botname> <any message>
    if ircmsg.find(bytes(":Hello %s" % botnick, "UTF-8")) != -1 or ircmsg.find(bytes(":hello %s" % botnick, "UTF-8")) != -1:
        modules.speak.hello()

    # !help
    if re.search(help_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!help")
            modules.help.display_help(input_string)
        except (AttributeError, ValueError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!help")

    # !imdb <Guessed Title>{#<Year>} // !imdb id:<imdbID>
    if re.search(imdb_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!imdb")
            modules.imdb.imdb_info(input_string)
        except (AttributeError, ValueError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!imdb")

    # !meet <Continent/City> <HH:MM>
    if re.search(meet_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!meet")
            modules.time.give_hour_equivalence(input_string)
        except (AttributeError, ValueError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!meet")

    # !op REGEX
    if re.search(op_regex, ircmsg, re.IGNORECASE):
        modules.connection.send_message("Nice try!")

    # !money <number> <CODE1>:<CODE2>
    if re.search(money_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!money")
            modules.money.money_rate(input_string)
        except (AttributeError, ValueError, IndexError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!money")

    # !quit REGEX
    if re.search(quit_user_regex, ircmsg, re.IGNORECASE):
        if is_message_from_admin(ircmsg):  # Catch if a bot admin is at the origin of the message
            modules.connection.send_message("Bye bye bitches!")
            quit()
        else:
            modules.connection.send_message("*rires*")

    # !say <something>
    if re.search(say_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!say")
            modules.speak.say(input_string)
        except (AttributeError, ValueError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!say")

    # !say <something>
    if re.search(say_private_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!say")
            modules.speak.say(input_string)
        except (AttributeError, ValueError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!say")

    # !steamprice <Game Title>
    if re.search(steamprice_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!steamprice")
            modules.steam.steam_price(input_string)
        except (AttributeError, ValueError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!steamprice")

    # !time <Continent/City>
    if re.search(time_regex, ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(ircmsg, "!time")
            modules.time.give_time(input_string)
        except (AttributeError, ValueError):
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!time")
