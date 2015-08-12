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
import re  # REGEX compiler

# Project modules
import modules.steam  # Contains specific Steam-Valve related functions
import modules.money
import modules.time
import modules.speak
import modules.connection


# # arguments ---------------------------------------------------------------------
# -s <server>  -c "<channel>" -b <bot nickname>
# parser = argparse.ArgumentParser(description='bbot, a bot without limits')
# parser.add_argument("-s", "--server", help="Server name", required=True)
# parser.add_argument("-c", "--channel", help="Channel name", required=True)
# parser.add_argument("-b", "--botnick", help="bbot nickname", required=True)
# args = parser.parse_args()
#
# # Creation of a config file
# with open('config.py', 'w+') as f:
#     f.write("import socket\n")
#     f.write("ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
#     f.write("server = '%s'\n" % args.server)
#     f.write("channel = '%s'\n" % args.channel)
#     f.write("botnick = '%s'\n" % args.botnick)

# Project config
import config  # Parsed variables from command line


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


# connect and join the configured channel
modules.connection.join_chan(config.channel)

# data reception ---------------------------------------------------------------
# Receive all the data from the server & channel
while 1:  # infinite loop
    ircmsg = modules.connection.receive_data()  # Receive data from the server
    ircmsg = ircmsg.strip(bytes("\n\r", "UTF-8"))  # removes unnecessary linebreaks
    print(ircmsg)  # DEBUG: print output of the channel

    # tracks PING : if the server pings the bot, it will answer
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1:
        modules.connection.ping()

    # tracks "Hello <botname> <any message>"
    if ircmsg.find(bytes(":Hello %s" % config.botnick, "UTF-8")) != -1:
        modules.speak.hello()

    # tracks "!time <Continent/City>"
    if ircmsg.find(bytes(":!time", "UTF-8")) != -1:
        try:
            # time_zone = 'Australia/Sydney'
            input_string = regex_coder(ircmsg, ":!time\s", 3)
            modules.time.give_time(input_string)
        except:
            modules.connection.send_message("Usage: !time <time_zones>")
            modules.connection.send_message("Purpose: Give the time in the specified time zone")
            modules.connection.send_message("Tip: Valid time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")

    # tracks "!meet <Continent/City> <HH:MM>"
    if ircmsg.find(bytes(":!meet", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!meet\s", 3)
            modules.time.give_hour_equivalence(input_string)
        except:
            modules.connection.send_message("Usage: !meet utc <HH:MM>")
            modules.connection.send_message("Purpose: Give the equivalence of the specified utc time input in several time zones")
            modules.connection.send_message("Tip: Only utc time zone works at this moment")

    # tracks "!money <number> <CODE1>:<CODE2>"
    if ircmsg.find(bytes(":!money", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!money\s", 3)
            modules.money.money_rate(input_string)
        except:
            modules.connection.send_message("Usage: !money <number> <CODE1>:<CODE2>")
            modules.connection.send_message("Purpose: Convert an amount from one currency to another")
            modules.connection.send_message("Tip: Valid currency codes: https://en.wikipedia.org/wiki/ISO_4217")

    # tracks "!say <something>"
    if ircmsg.find(bytes(":!say", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!say\s", 3)
            modules.speak.say(input_string)
        except:
            modules.connection.send_message("Usage: !say <something>")

        # tracks "!steamprice <Game Title>"
    if ircmsg.find(bytes(":!steamprice", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!steamprice\s", 3)
            modules.steam.steam_price(input_string)
        except:
            modules.connection.send_message("Usage: !steamprice <Game Title>")
            modules.connection.send_message("Purpose: Give the price of the given Steam game")
            modules.connection.send_message("Tip: Title must be exact")
