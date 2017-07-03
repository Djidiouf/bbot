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
import modules.youtube
import modules.calc
import modules.translate


# conf = configparser.RawConfigParser()
# conf.add_section('bot_configuration')
# conf.set('bot_configuration', 'server', args.server)
# conf.set('bot_configuration', 'channel', args.channel)
# conf.set('bot_configuration', 'botnick', args.botnick)

# # Writing our configuration file to 'example.cfg'
# with open('config.cfg', 'w') as configfile:
#     conf.write(configfile)

# Variables
debug = True

# Read config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))  # Absolute path is better
server = config['bot_configuration']['server']
channel = config['bot_configuration']['channel']
botnick = config['bot_configuration']['botnick']
# admins_list = config.get('bot_configuration', 'admin')
admins_list = config['bot_configuration']['admins'].split(",")
ignored_users = config['bot_configuration']['ignored_users'].split(",")

# ip_format = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # IP check
ip_format = r"([^\s]+)"  # Thx to IRC specifications >:(

user_message = r"(.*)!(.*)" + r"@" + ip_format                                 # Match: User!~User@123.123.123.123


# REGEX ----------------------------------------------------------------------------------------------------------------
# Scan if command made directly to botnick or to channel
botnick_regex = user_message + r" PRIVMSG " + re.escape(botnick) + r" :"

channel_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :"

# commands
# !calc
calc_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!calc"

# !help
help_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!help"

# !imdb
imdb_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!imdb"

# !meet
meet_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!meet"

# !money
money_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!money"

# !op
op_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!op"

# !quit
quit_user_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!quit"

# !say
say_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!say"

# !say (In private: /msg botnick !say)
say_private_regex = user_message + r" PRIVMSG " + re.escape(botnick) + r" :" + r"!say"

# !steam
steamprice_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!steam"

# !steamadmin
steamadmin_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!steamadmin"

# !steamown
steamown_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!steamown"

# !time
time_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!time"

# !yt
yt_regex = user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!yt"


def regex_search_arguments(message, expression):
    arguments_regex = '(?<=' + re.escape(expression) + ' )(.*)'
    string_searched = re.search(arguments_regex, message, re.IGNORECASE)
    # print("string_searched =", string_searched)  # DEBUG: <_sre.SRE_Match object; span=(65, 75), match='15 EUR:AUD'>
    arguments = string_searched.group(0)
    return arguments

def report_error(i_cmd, i_error, i_msg, i_admins_list, is_help_needed=False):
    modules.connection.send_message(("Call %s: %s" % (i_cmd, i_msg)), "private", i_admins_list)
    modules.connection.send_message(("Error %s: %s" % (i_cmd, i_error)), "private", i_admins_list)

    if is_help_needed:
        modules.help.display_help(i_cmd, "error")


# connect and join the configured channel
modules.connection.join_chan(channel)

# data reception ---------------------------------------------------------------
# Receive all the data from the server & channel
while 1:  # infinite loop
    ircmsg = modules.connection.receive_data()  # Receive data from the server
    ircmsg = ircmsg.strip(bytes("\n\r", "UTF-8"))  # Remove linebreaks which appear on each message
    decoded_ircmsg = ircmsg.decode('utf-8')  # decode ircmsg from binary to string

    # DEBUG: print output of the channel
    if debug:
        # print(ircmsg)         # binary
        print(decoded_ircmsg)   # string

    # TRACKS -----------------------------------------------------------------------------------------------------------
    # PING : if the server pings the bot, it will answer
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1:
        modules.connection.ping()

    # Determine if private message or channel
    try:
        medium_used_regex = user_message + r" PRIVMSG " + r'.*' + r'(?=.:)'
        medium_used_searched = re.search(medium_used_regex, decoded_ircmsg, re.IGNORECASE)
        medium_used = medium_used_searched.group(0).split()[-1]  # split the last word of matching pattern in regex
        # user_talking_beta = medium_used_searched.group(1)[1:]  # [1:] removes first character (which is btw, a : )
        # print(user_talking_beta)
        # print(medium_used)
    except:
        pass

    # User talking retrieval
    try:
        user_talking_regex = r'(.*)' + r'(?=!.*@)'
        user_talking_searched = re.search(user_talking_regex, decoded_ircmsg, re.IGNORECASE)
        user_talking = user_talking_searched.group(0)[1:]  # [1:] removes first character (which is btw, a : )
        # print(user_talking)
    except:
        # message must be a system server message
        continue

    # Ignore specific users
    if user_talking:
        if user_talking in ignored_users:
            continue

    # INLINE -----------------------------------------------------------------------------------------------------------
    # Hello <botname> <any message>
    if decoded_ircmsg.find(":Hello %s" % botnick) != -1 or decoded_ircmsg.find(":hello %s" % botnick) != -1:
        modules.speak.hello()

    # linkinline
    if decoded_ircmsg.find("http://") != -1 or decoded_ircmsg.find("https://") != -1:
        try:
            modules.translate.translate_inline(decoded_ircmsg)
            pass
        except:
            report_error("linkinline", sys.exc_info()[0], decoded_ircmsg, admins_list[0], False)

    # steaminline
    if decoded_ircmsg.find("http://store.steampowered.com/app/") != -1 or decoded_ircmsg.find(
            "https://store.steampowered.com/app/") != -1:
        try:
            modules.steam.steam_inline(decoded_ircmsg)
            pass
        except:
            report_error("steaminline", sys.exc_info()[0], decoded_ircmsg, admins_list[0], False)

    # COMMANDS ---------------------------------------------------------------------------------------------------------
    # !help
    if re.search(help_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!help")
            modules.help.display_help(input_string, "detailed")
            continue
        except:
            report_error("!help", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !calc <operations>
    if re.search(calc_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!calc")
            modules.calc.main(input_string)
            continue
        except:
            report_error("!calc", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !imdb <Guessed Title>{#<Year>} // !imdb id:<imdbID>
    if re.search(imdb_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!imdb")
            modules.imdb.imdb_info(input_string)
            continue
        except:
            report_error("!imdb", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !meet <Continent/City> <HH:MM>
    if re.search(meet_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!meet")
            modules.time.give_hour_equivalence(input_string)
            continue
        except:
            report_error("!meet", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !money <number> <CODE1>:<CODE2>
    if re.search(money_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!money")
            modules.money.money_rate(input_string)
            continue
        except:
            report_error("!money", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !op REGEX
    if re.search(op_regex, decoded_ircmsg, re.IGNORECASE):
        modules.connection.send_message("Nice try!")
        continue

    # !quit REGEX
    if re.search(quit_user_regex, decoded_ircmsg, re.IGNORECASE):
        if user_talking:
            if user_talking in admins_list:
                modules.connection.send_message("Bye bye bitches!")
                quit()
            else:
                modules.connection.send_message("*rires*")

    # !say <something>
    if re.search(say_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!say")
            modules.speak.say(input_string)
            continue
        except:
            report_error("!say", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !say <something privately>
    if re.search(say_private_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!say")
            modules.speak.say(input_string)
            continue
        except:
            report_error("!say private", sys.exc_info()[0], decoded_ircmsg, admins_list[0], False)

    # !steam <Game Title>
    if re.search(steamprice_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!steam")
            modules.steam.steam_price(input_string)
            continue
        except:
            report_error("!steam", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !steamadmin <admin command>
    if re.search(steamadmin_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!steamadmin")
            modules.steam.steam(input_string)
            continue
        except:
            report_error("!steamadmin", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !steamown <player> <Game>
    if re.search(steamown_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!steamown")
            modules.steam.player_owns_game(input_string)
            continue
        except:
            report_error("!steamown", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !time <Continent/City>
    if re.search(time_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!time")
            modules.time.main(input_string)
            continue
        except:
            report_error("!time", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)

    # !yt <ChannelID>
    if re.search(yt_regex, decoded_ircmsg, re.IGNORECASE):
        try:
            input_string = regex_search_arguments(decoded_ircmsg, "!yt")
            modules.youtube.main(input_string)
            continue
        except:
            report_error("!yt", sys.exc_info()[0], decoded_ircmsg, admins_list[0], True)
