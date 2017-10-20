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
import time

# Project modules
import modules.steam  # Contains specific Steam-Valve related functions
import modules.money
import modules.time
import modules.speak
import modules.connection
import modules.help
import modules.imdb
import modules.youtube
import modules.aws
import modules.aws_sqs
import modules.calc
import modules.translate
import modules.ping


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
aws_allowed_users = config['aws']['allowed_users'].split(",")

# ip_format = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # IP check
ip_format = r"([^\s]+)"  # Thx to IRC specifications >:(

user_message = r"(.*)!(.*)" + r"@" + ip_format                                 # Match: User!~User@123.123.123.123


# REGEX ----------------------------------------------------------------------------------------------------------------
# Scan if command made directly to botnick or to channel
botnick_regex = user_message + r" PRIVMSG " + re.escape(botnick) + r" :"

channel_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :"

# commands
# !aws
aws_regex = user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!aws"

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

# !ping
ping_user_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!ping"

# !quit
quit_user_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :" + r"!quit"

# !say
say_regex = user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!say"

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
# yt_regex_compiled = re.compile(yt_regex, re.IGNORECASE)


def regex_search_arguments(message, expression):
    arguments_regex = '(?<=' + re.escape(expression) + ' )(.*)'
    string_searched = re.search(arguments_regex, message, re.IGNORECASE)
    # print("string_searched =", string_searched)  # DEBUG: <_sre.SRE_Match object; span=(65, 75), match='15 EUR:AUD'>
    arguments = string_searched.group(0)
    return arguments


def report_error(i_cmd, i_error, i_msg, i_medium, i_admin):
    modules.connection.send_message(("Call %s: %s" % (i_cmd, i_msg)), i_medium, i_admin)
    modules.connection.send_message(("Error %s: %s" % (i_cmd, i_error)), i_medium, i_admin)


# connect and join the configured channel
modules.connection.join_chan(channel)

# data reception ---------------------------------------------------------------
# Receive all the data from the server & channel
while 1:  # infinite loop
    ircmsg = modules.connection.receive_data()  # Receive data from the server
    if len(ircmsg) == 0:
        print("Disconnection detected. Attempt to reconnect...")
        time.sleep(5)  # Be easy on the reconnection
        modules.connection.join_chan(channel)

    ircmsg = ircmsg.strip(bytes("\n\r", "UTF-8"))  # Remove linebreaks which appear on each message
    decoded_ircmsg = ircmsg.decode('utf-8')  # decode ircmsg from binary to string

    # DEBUG: print output of the channel
    if debug:
        # print(ircmsg)         # binary
        print(decoded_ircmsg)   # string

    # PING : if the server pings the bot, it will answer - Happens every 2min30 on freenode.net
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1:
        modules.connection.ping()

    # AWS SQS Queue ----------------------------------------------------------------------------------------------------
    # Poll Given SQS queue
    if config['aws']['sqs_queue']:
        # print("A polling is made")
        cmd = "SQS - Retrieve message"
        try:
            modules.aws_sqs.main()
            pass
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])

    # METADATA ---------------------------------------------------------------------------------------------------------
    # Parse decoded_ircmsg for metadata
    try:
        metadata_regex = user_message + r" PRIVMSG " + r'.*' + r'(?=.:)'
        metadata_searched = re.search(metadata_regex, decoded_ircmsg, re.IGNORECASE)
        medium_used = metadata_searched.group(0).split()[-1]  # split the last word of matching pattern in regex
        alias_talking = metadata_searched.group(1)[1:]  # [1:] removes first character (which is btw, a : )
        user_talking = metadata_searched.group(2)[1:]  # [1:] removes first character (which is btw, a ~ )
        user_ip = metadata_searched.group(3)

        if user_talking in ignored_users:  # Ignore specific users whatever alias they have
            continue
    except:
        # message must be a system server message
        continue

    # INLINE -----------------------------------------------------------------------------------------------------------
    # Hello <botname> <any message>
    if decoded_ircmsg.find(":Hello %s" % botnick) != -1 or decoded_ircmsg.find(":hello %s" % botnick) != -1:
        modules.speak.hello()

    # linkinline
    if decoded_ircmsg.find("http://") != -1 or decoded_ircmsg.find("https://") != -1:
        try:
            modules.translate.main(decoded_ircmsg, medium_used, alias_talking)
            pass
        except:
            report_error("linkinline", sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])

    # steaminline
    if decoded_ircmsg.find("http://store.steampowered.com/app/") != -1 or decoded_ircmsg.find(
            "https://store.steampowered.com/app/") != -1:
        try:
            url_searched = re.search("https?://[^\s]+", decoded_ircmsg, re.IGNORECASE)
            modules.steam.steam_inline(url_searched.group(0))
            pass
        except:
            report_error("steaminline", sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])

    # COMMANDS ---------------------------------------------------------------------------------------------------------
    # !help
    if re.search(help_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!help"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.help.display_help(input_string, "detailed")
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !aws <operations>
    if re.search(aws_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!aws"

        if user_talking:
            if user_talking in aws_allowed_users:
                try:
                    input_string = regex_search_arguments(decoded_ircmsg, cmd)
                    modules.aws.main(input_string, medium_used, alias_talking)
                    continue
                except:
                    report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
                    modules.help.display_help(cmd, "error", medium_used, alias_talking)
            else:
                modules.connection.send_message("Sorry, you are not allowed to use this command.")

    # !calc <operations>
    if re.search(calc_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!calc"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.calc.main(input_string)
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !imdb <Guessed Title>{#<Year>} // !imdb id:<imdbID>
    if re.search(imdb_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!imdb"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.imdb.imdb_info(input_string)
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !meet <Continent/City> <HH:MM>
    if re.search(meet_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!meet"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.time.give_hour_equivalence(input_string)
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !money <number> <CODE1>:<CODE2>
    if re.search(money_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!money"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.money.money_rate(input_string)
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !op REGEX
    if re.search(op_regex, decoded_ircmsg, re.IGNORECASE):
        modules.connection.send_message("Nice try!")
        continue

    # !ping
    if re.search(ping_user_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!ping"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.ping.main(input_string)
        except:
            modules.ping.main(user_ip)

    # !quit REGEX
    if re.search(quit_user_regex, decoded_ircmsg, re.IGNORECASE):
        if user_talking:
            if user_talking in admins_list:
                modules.connection.send_message("Bye bye bitches!")
                sys.exit("Bot admin requested a shutdown.")
            else:
                modules.connection.send_message("*rires*")

    # !say <something>
    if re.search(say_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!say"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.speak.say(input_string)
            continue
        except:
            report_error("%s (%s)" % (cmd, medium_used), sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !steam <Game Title>
    if re.search(steamprice_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!steam"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.steam.steam_price(input_string)
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !time <Continent/City>
    if re.search(time_regex, decoded_ircmsg, re.IGNORECASE):
        cmd = "!time"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.time.main(input_string)
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)

    # !yt <ChannelID>
    if re.search(yt_regex, decoded_ircmsg, re.IGNORECASE):
    # if yt_regex_compiled.search(decoded_ircmsg):
        cmd = "!yt"
        try:
            input_string = regex_search_arguments(decoded_ircmsg, cmd)
            modules.youtube.main(input_string, medium_used, alias_talking)
            continue
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])
            modules.help.display_help(cmd, "error", medium_used, alias_talking)


