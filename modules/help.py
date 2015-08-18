__author__ = 'Djidiouf'

# Project modules
import modules.connection


def print_help_help():
    modules.connection.send_message("Usage: !help [handler]")
    modules.connection.send_message("Known handlers:")
    modules.connection.send_message("!help !imdb !meet !money !quit !say !steamprice !time")


def display_help(i_string):

    if i_string == "!help":
        print_help_help()
    elif i_string == "!imdb":
        modules.connection.send_message("Usage: !imdb <Guessed Title>")
        modules.connection.send_message("Usage: !imdb <Guessed Title>#<Year>")
        modules.connection.send_message("Usage: !imdb id:<imdbID>")
        modules.connection.send_message("Purpose: Give information about a movie / TV serie")
        modules.connection.send_message("Tip: Title you enter is a guessed title, specify the year for more accuracy")
    elif i_string == "!meet":
        modules.connection.send_message("Usage: !meet utc <HH:MM>")
        modules.connection.send_message("Purpose: Give the equivalence of the specified time input in several time zones")
        modules.connection.send_message("Tip: Only utc time zone works at this moment")
    elif i_string == "!money":
        modules.connection.send_message("Usage: !money <number> <CODE1>:<CODE2>")
        modules.connection.send_message("Purpose: Convert an amount from one currency to another")
        modules.connection.send_message("Tip: Valid currency codes: https://en.wikipedia.org/wiki/ISO_4217")
    elif i_string == "!quit":
        modules.connection.send_message("Usage: !quit")
        modules.connection.send_message("Purpose: Make me quit IRC")
        modules.connection.send_message("Tip: Don't be mean with me please :'(")
    elif i_string == "!say":
        modules.connection.send_message("Usage: !say <something>")
        modules.connection.send_message("Purpose: Make me speak!")
        modules.connection.send_message("Tip: Be smart and /msg myname the command")
    elif i_string == "!steamprice":
        modules.connection.send_message("Usage: !steamprice <Game Title>")
        modules.connection.send_message("Purpose: Give the price of the given Steam game")
        modules.connection.send_message("Tip: Title must be exact")
    elif i_string == "!time":
        modules.connection.send_message("Usage: !time <time_zones>")
        modules.connection.send_message("Purpose: Give the time in the specified time zone")
        modules.connection.send_message("Tip: Valid time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
    else:
        print_help_help()
