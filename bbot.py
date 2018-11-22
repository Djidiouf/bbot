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
import configparser
import re  # REGEX compiler
import sys  # system library
import os
import time
import importlib
import chardet  # detect encoding

# Project modules
import modules.aws
import modules.aws_sqs
import modules.calc
import modules.finance
import modules.connection
import modules.help
import modules.imdb
import modules.meet
import modules.money
import modules.money_inline
import modules.ping
import modules.quit
import modules.speak
import modules.steam
import modules.time
import modules.translate
import modules.youtube


# Read config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))  # Absolute path is better
server = config['bot_configuration']['server']
channel = config['bot_configuration']['channel']
botnick = config['bot_configuration']['botnick']
admins_list = config['bot_configuration']['admins'].split(",")
ignored_users = config['bot_configuration']['ignored_users'].split(",")
debug_mode = config['modes']['debug']

authorised_handlers = config['bot_configuration']['authorised_handlers'].split(",")
authorised_features = config['bot_configuration']['authorised_features'].split(",")

# ip_format = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # IP check
ip_format = r"([^\s]+)"  # Thx to IRC specifications >:(
user_message = r"(.*)!(.*)" + r"@" + ip_format                                 # Match: User!~User@123.123.123.123


# REGEX ----------------------------------------------------------------------------------------------------------------
# Scan if command made directly to botnick or to channel
botnick_regex = user_message + r" PRIVMSG " + re.escape(botnick) + r" :"
channel_regex = user_message + r" PRIVMSG " + re.escape(channel) + r" :"

# Regex
aws_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!aws")
calc_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!calc")
finance_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!finance")
help_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!help")
imdb_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!imdb")
meet_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!meet")
money_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!money")
ping_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!ping")
quit_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!quit")
say_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!say")
steam_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!steam")
time_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!time")
yt_regex = re.compile(user_message + r" PRIVMSG " + r"(" + re.escape(channel) + r"|" + re.escape(botnick) + r")" + r" :" + r"!yt")

money_inline_regex = re.compile(r"(?:A\$|\$|\€|\£)[0-9|\,|\.|\s|\']+|(?:\d\s|\d|\.\d)[0-9|\,|\.|\s|\']*[a-zA-Z]{3}\b|\d[0-9|\,|\.|\'|\s]*(?:A\$|\$|\s\$|\€|\£)")  # https://regex101.com/r/eI8wlW/7


def regex_search_arguments(message, expression):
    try:
        arguments_regex = '(?<=' + re.escape(expression) + ' )(.*)'
        string_searched = re.search(arguments_regex, message, re.IGNORECASE)
        # print("string_searched =", string_searched)  # DEBUG: <_sre.SRE_Match object; span=(65, 75), match='15 EUR:AUD'>
        arguments = string_searched.group(0)
        return arguments
    except:
        arguments = False
        return arguments


def report_error(i_cmd, i_error, i_msg, i_medium, i_admin):
    modules.connection.send_message(("Call %s: %s" % (i_cmd, i_msg)), i_medium, i_admin)
    modules.connection.send_message(("Error %s: %s" % (i_cmd, i_error)), i_medium, i_admin)


def cmd_multichan(i_cmd, i_module, i_decoded_ircmsg, i_medium, i_alias, i_botnick, i_admin, i_input_sub=None, i_input_add=None):
    try:
        module = importlib.import_module('modules.%s' % i_module)
        i_input = regex_search_arguments(i_decoded_ircmsg, i_cmd)
        if i_input:
            if i_input_add:
                getattr(module, 'main')(i_input, i_input_add, i_medium, i_alias)
            else:
                getattr(module, 'main')(i_input, i_medium, i_alias)
        elif i_input is False and i_input_sub is not None:
            i_input = i_input_sub
            getattr(module, 'main')(i_input, i_medium, i_alias)
        else:
            modules.help.main(i_cmd, "error", i_medium, i_alias)
    except Exception:
        report_error("%s (%s)" % (i_cmd, i_medium), sys.exc_info()[0], i_decoded_ircmsg, i_botnick, i_admin)
        modules.help.main(i_cmd, "error", i_medium, i_alias)


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

    # Decode binary (try first using utf-8 before trying to guess the encoding)
    encoding = chardet.detect(ircmsg)['encoding']   # Detect encoding used

    try:
        ircmsg = ircmsg.strip(bytes("\n\r", 'utf-8'))   # Remove linebreaks which appear on each message
        decoded_ircmsg = ircmsg.decode('utf-8')         # decode ircmsg from binary to string
    except UnicodeDecodeError:
        ircmsg = ircmsg.strip(bytes("\n\r", encoding))  # Remove linebreaks which appear on each message
        decoded_ircmsg = ircmsg.decode(encoding)        # decode ircmsg from binary to string

    # DEBUG: print output of the channel
    if debug_mode:
        # print(ircmsg)         # binary
        print(decoded_ircmsg)   # string

    # METADATA ---------------------------------------------------------------------------------------------------------
    # Parse decoded_ircmsg for metadata
    try:
        metadata_regex = user_message + r" PRIVMSG " + r'.*' + r'(?=.:)'
        metadata_searched = re.search(metadata_regex, decoded_ircmsg, re.IGNORECASE)
        medium_used = metadata_searched.group(0).split()[2]  # retrieve second matching pattern
        alias_talking = metadata_searched.group(1)[1:]  # [1:] removes first character (which is btw, a : )
        user_talking = metadata_searched.group(2)[1:]  # [1:] removes first character (which is btw, a ~ )
        user_ip = metadata_searched.group(3)

        if user_talking in ignored_users:  # Ignore specific users whatever alias they have
            continue
    except:
        # message must be a system server message
        if ircmsg.find(bytes("PING :", encoding)) != -1:  # Answer to PING message - Happens every 2min30 on freenode.net
            modules.connection.ping()
            # continue  # need to not continue/pass to get the SQS queue working every 2.30minute
        else:  # do not process any other system message
            continue

    # FEATURES ---------------------------------------------------------------------------------------------------------
    # AWS SQS Queue - Poll Given SQS queue
    if "aws_sqs" in authorised_features and config['aws']['sqs_queue']:
        cmd = "SQS - Retrieve message"
        try:
            modules.aws_sqs.main()
            pass
        except:
            report_error(cmd, sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])

    # Hello <botname> <any message>
    if decoded_ircmsg.find(":Hello %s" % botnick) != -1 or decoded_ircmsg.find(":hello %s" % botnick) != -1:
        modules.speak.hello()

    # linkinline
    if "linkinline" in authorised_features:
        if decoded_ircmsg.find("http://") != -1 or decoded_ircmsg.find("https://") != -1:
            try:
                modules.translate.main(decoded_ircmsg, medium_used, alias_talking)
                pass
            except:
                report_error("linkinline", sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])

    # steaminline
    if "steaminline" in authorised_features:
        if decoded_ircmsg.find("http://store.steampowered.com/app/") != -1 or decoded_ircmsg.find(
                "https://store.steampowered.com/app/") != -1:
            try:
                url_searched = re.search("https?://[^\s]+", decoded_ircmsg, re.IGNORECASE)
                modules.steam.steam_inline(url_searched.group(0), medium_used, alias_talking)
                pass
            except:
                report_error("steaminline", sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])

    # money_inline
    if "money_inline" in authorised_features:
        if money_inline_regex.search(decoded_ircmsg, re.IGNORECASE):
        #if any(char.isdigit() for char in decoded_ircmsg):
            try:
                modules.money_inline.main(decoded_ircmsg, medium_used, alias_talking)
                pass
            except:
                report_error("money_inline", sys.exc_info()[0], decoded_ircmsg, botnick, admins_list[0])

    # HANDLERS ---------------------------------------------------------------------------------------------------------
    if "!aws" in authorised_handlers and aws_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!aws", "aws", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!calc" in authorised_handlers and calc_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!calc", "calc", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!finance" in authorised_handlers and finance_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!finance", "finance", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!help" in authorised_handlers and help_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!help", "help", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0], i_input_add="detailed")

    if "!imdb" in authorised_handlers and imdb_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!imdb", "imdb", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!meet" in authorised_handlers and meet_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!meet", "meet", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!money" in authorised_handlers and money_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!money", "money", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!ping" in authorised_handlers and ping_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!ping", "ping", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0], i_input_sub=user_ip)

    if "!quit" in authorised_handlers and quit_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!quit", "quit", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0], i_input_sub="unset")

    if "!say" in authorised_handlers and say_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!say", "speak", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!steam" in authorised_handlers and steam_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!steam", "steam", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!time" in authorised_handlers and time_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!time", "time", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])

    if "!yt" in authorised_handlers and yt_regex.search(decoded_ircmsg, re.IGNORECASE):
        cmd_multichan("!yt", "youtube", decoded_ircmsg, medium_used, alias_talking, botnick, admins_list[0])
