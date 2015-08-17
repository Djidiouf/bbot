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

conf = configparser.RawConfigParser()
conf.read('config.cfg')
server = conf.get('bot_configuration', 'server')
channel = conf.get('bot_configuration', 'channel')
botnick = conf.get('bot_configuration', 'botnick')
admin = conf.get('bot_configuration', 'admin')


ip_format = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
admin_message = re.escape(admin) + r"!~" + re.escape(admin) + r"@" + ip_format  # Match: EveryAdmin!~EveryAdmin@123.123.123.123
user_message = r"(.*)!~(.*)" + r"@" + ip_format  # Match: EveryUser!~EveryUser@123.123.123.123

quit_regex = admin_message + r" PRIVMSG " + re.escape(channel) +  r" :" + r"!quit"
quit_regex = bytes(quit_regex, "UTF-8")

op_regex = user_message + r" PRIVMSG " + re.escape(channel) +  r" :" + r"!op"
op_regex = bytes(op_regex, "UTF-8")


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

    # !help
    if ircmsg.find(bytes(":!help", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!help\s", 3)
            modules.help.display_help(input_string)
        except:
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!help")

    # Hello <botname> <any message>
    if ircmsg.find(bytes(":Hello %s" % botnick, "UTF-8")) != -1 or ircmsg.find(bytes(":hello %s" % botnick, "UTF-8")) != -1:
        modules.speak.hello()

    # !time <Continent/City>
    if ircmsg.find(bytes(":!time", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!time\s", 3)
            modules.time.give_time(input_string)
        except:
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!time")

    # !meet <Continent/City> <HH:MM>
    if ircmsg.find(bytes(":!meet", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!meet\s", 3)
            modules.time.give_hour_equivalence(input_string)
        except:
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!meet")

    # !money <number> <CODE1>:<CODE2>
    if ircmsg.find(bytes(":!money", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!money\s", 3)
            modules.money.money_rate(input_string)
        except:
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!money")

    # !say <something>
    if ircmsg.find(bytes(":!say", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!say\s", 3)
            modules.speak.say(input_string)
        except:
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!say")

    # !steamprice <Game Title>
    if ircmsg.find(bytes(":!steamprice", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!steamprice\s", 3)
            modules.steam.steam_price(input_string)
        except:
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!steamprice")

    # !imdb <Guessed Title>{#<Year>} // !imdb id:<imdbID>
    if ircmsg.find(bytes(":!imdb", "UTF-8")) != -1:
        try:
            input_string = regex_coder(ircmsg, ":!imdb\s", 3)
            modules.imdb.imdb_info(input_string)
        except:
            error = sys.exc_info()[0]
            print("Error: %s" % error)
            modules.help.display_help("!imdb")

    # !quit
    if ircmsg.find(bytes(admin + "!~Djidiouf@203.210.68.172" + " PRIVMSG " + channel + " :!quit", "UTF-8")) != -1:
        print("quit message")
        #quit()

    # !quit REGEX
    if re.search(quit_regex, ircmsg, re.IGNORECASE):
        #DEBUG print("REGEX quit message")
        modules.connection.send_message("Bye bye bitch!")
        quit()
    # !quit REGEX
    if re.search(quit_regex, ircmsg, re.IGNORECASE):
        #DEBUG print("REGEX quit message")
        modules.connection.send_message("Bye bye bitches!")
        quit()

    # !quit REGEX
    if re.search(op_regex, ircmsg, re.IGNORECASE):
        modules.connection.send_message("Nice try!")
