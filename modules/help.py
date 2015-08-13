__author__ = 'Djidiouf'

# Project modules
import modules.connection


def display_help(i_string):

    if i_string == "!time":
        modules.connection.send_message("Usage: !time <time_zones>")
        modules.connection.send_message("Purpose: Give the time in the specified time zone")
        modules.connection.send_message("Tip: Valid time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
    elif i_string == "!meet":
        modules.connection.send_message("Usage: !meet utc <HH:MM>")
        modules.connection.send_message("Purpose: Give the equivalence of the specified utc time input in several time zones")
        modules.connection.send_message("Tip: Only utc time zone works at this moment")
    elif i_string == "!money":
        modules.connection.send_message("Usage: !money <number> <CODE1>:<CODE2>")
        modules.connection.send_message("Purpose: Convert an amount from one currency to another")
        modules.connection.send_message("Tip: Valid currency codes: https://en.wikipedia.org/wiki/ISO_4217")
    elif i_string == "!say":
        modules.connection.send_message("Usage: !say <something>")
        modules.connection.send_message("Purpose: Make me speak!")
        modules.connection.send_message("Tip: Be smart and /msg me the command")
    elif i_string == "!steamprice":
        modules.connection.send_message("Usage: !steamprice <Game Title>")
        modules.connection.send_message("Purpose: Give the price of the given Steam game")
        modules.connection.send_message("Tip: Title must be exact")
    elif i_string == "!help":
        modules.connection.send_message("Usage: !help")
        modules.connection.send_message("Usage: !help <command>")
        modules.connection.send_message("Purpose: Give specific information about a command")
        modules.connection.send_message("Tip: Help yourself if !help is not enough for you")
    else:
        modules.connection.send_message("Commands available:")
        modules.connection.send_message("!help <command>")
        modules.connection.send_message("!meet utc <HH:MM>")
        modules.connection.send_message("!money <number> <CODE1>:<CODE2>")
        modules.connection.send_message("!say <something>")
        modules.connection.send_message("!steamprice <Game Title>")
        modules.connection.send_message("!time <time_zones>")
