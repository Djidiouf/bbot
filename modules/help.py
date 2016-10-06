__author__ = 'Djidiouf'

# Project modules
import modules.connection


def print_help_help():
    modules.connection.send_message("Usage: !help <handler>")
    modules.connection.send_message("Known handlers:")
    modules.connection.send_message("!help !imdb !meet !money !quit !say !steam !steamadmin !steamown !steamprice !time !yt")


def display_help(i_string, mode):

    if i_string == "!help":
        print_help_help()
    elif i_string == "!calc":
        modules.connection.send_message("Usage: !calc <Operations>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Compute things faster than you")
            modules.connection.send_message("Tip: Functions available > https://docs.python.org/3/library/math.html")
    elif i_string == "!imdb":
        modules.connection.send_message("Usage: !imdb <Guessed Title>")
        modules.connection.send_message("Usage: !imdb <Guessed Title>#<Year>")
        modules.connection.send_message("Usage: !imdb id:<imdbID>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give information about a movie / TV serie")
            modules.connection.send_message("Tip: Title you enter is a guessed title, specify the year for more accuracy")
    elif i_string == "!meet":
        modules.connection.send_message("Usage: !meet <TimeZone> <HH:MM>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give the equivalence of the specified time input in several time zones")
            modules.connection.send_message("Tip: Valid time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
    elif i_string == "!money":
        modules.connection.send_message("Usage: !money <number> <CODE1>:<CODE2>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Convert an amount from one currency to another")
            modules.connection.send_message("Tip: Valid currency codes: https://en.wikipedia.org/wiki/ISO_4217")
    elif i_string == "!quit":
        modules.connection.send_message("Usage: !quit")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Make me quit IRC")
            modules.connection.send_message("Tip: Don't be mean with me please :'(")
    elif i_string == "!say":
        modules.connection.send_message("Usage: !say <something>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Make me speak!")
            modules.connection.send_message("Tip: Be smart and /msg me the command privately")
    elif i_string == "!steamadmin":
        modules.connection.send_message("Usage: !steam <Admin Command>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Let do super-things")
    elif i_string == "!steamown":
        modules.connection.send_message("Usage: !steamown <player> <Game>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Tell if someone owns a specific game")
            modules.connection.send_message("Tip: Player name and title must be exact")
    elif i_string == "!steamprice":
        modules.connection.send_message("Usage: !steamprice <Game Title>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give the price of the given Steam game")
            modules.connection.send_message("Tip: Title must be exact")
    elif i_string == "!time":
        modules.connection.send_message("Usage: !time <TimeZone>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give the time in the specified time zone")
            modules.connection.send_message("Tip: Get valid timezones of a country with: !time <two-letter-country-code>")
            modules.connection.send_message("---- Countries' codes: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2")
    elif i_string == "!yt":
        modules.connection.send_message("Usage: !yt <Display name or ID>")
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give metadata about a YouTube Channel")
    else:
        print_help_help()
