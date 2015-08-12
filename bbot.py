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
import modules.messages
import modules.money
import modules.time
import modules.speak


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


# functions ---------------------------------------------------------------------
# functions that will do the handling of the servers's data

def ping():  # Respond to server pings
    config.ircsock.send(bytes("PONG :Pong\n", "UTF-8"))


def join_chan(chan):  # Join channel
    config.ircsock.send(bytes("JOIN %s\r\n" % chan, "UTF-8"))


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


# connection --------------------------------------------------------------------
# connect and join the configured channel
# ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config.ircsock.connect((config.server, 6667))  # Connect to port 6667

# Sends the username, real name etc : user authentication
config.ircsock.send(bytes("USER %s %s %s :%s\r\n" % (config.botnick, config.botnick, config.botnick, config.botnick), "UTF-8"))

# Assignment of a nick to the bot
config.ircsock.send(bytes("NICK %s\r\n" % config.botnick, "UTF-8"))

# After connection, join the specified channel
join_chan(config.channel)


# data reception ---------------------------------------------------------------
# Receive all the data from the server & channel
while 1:  # infinite loop
    ircmsg = config.ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip(bytes("\n\r", "UTF-8"))  # removes unnecessary linebreaks
    print(ircmsg)  # DEBUG: print output of the channel

    # tracks PING : if the server pings the bot, it will answer
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1:
        ping()

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
            modules.messages.Message(config.channel).send_message("Usage: !time <time_zones>")
            modules.messages.Message(config.channel).send_message("Purpose: Give the time in the specified time zone")
            modules.messages.Message(config.channel).send_message("Tip: Valid time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")

    # tracks "!meet <Continent/City> <HH:MM>"
    if ircmsg.find(bytes(":!meet", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!meet\s", 3)
            modules.time.give_hour_equivalence(input_string)
        except:
            modules.messages.Message(config.channel).send_message("Usage: !meet utc <HH:MM>")
            modules.messages.Message(config.channel).send_message("Purpose: Give the equivalence of the specified utc time input in several time zones")
            modules.messages.Message(config.channel).send_message("Tip: Only utc time zone works at this moment")

    # tracks "!money <number> <CODE1>:<CODE2>"
    if ircmsg.find(bytes(":!money", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!money\s", 3)
            modules.money.money_rate(input_string)
        except:
            modules.messages.Message(config.channel).send_message("Usage: !money <number> <CODE1>:<CODE2>")
            modules.messages.Message(config.channel).send_message("Purpose: Convert an amount from one currency to another")
            modules.messages.Message(config.channel).send_message("Tip: Valid currency codes: https://en.wikipedia.org/wiki/ISO_4217")

    # tracks "!say <something>"
    if ircmsg.find(bytes(":!say", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!say\s", 3)
            modules.speak.say(input_string)
        except:
            modules.messages.Message(config.channel).send_message("Usage: !say <something>")

        # tracks "!steamprice <Game Title>"
    if ircmsg.find(bytes(":!steamprice", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!steamprice\s", 3)
            modules.steam.steam_price(input_string)
        except:
            modules.messages.Message(config.channel).send_message("Usage: !steamprice <Game Title>")
            modules.messages.Message(config.channel).send_message("Purpose: Give the price of the given Steam game")
            modules.messages.Message(config.channel).send_message("Tip: Title must be exact")
