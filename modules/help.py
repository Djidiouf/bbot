__author__ = 'Djidiouf'

# Project modules
import modules.connection


def print_help_help(i_medium=None, i_alias=None):
    modules.connection.send_message("Usage: !help <handler>", i_medium, i_alias)
    modules.connection.send_message("Known handlers:", i_medium, i_alias)
    modules.connection.send_message("!aws !calc !imdb !meet !money !ping !quit !say !steam !time !yt", i_medium, i_alias)


def display_help(i_string, mode, i_medium=None, i_alias=None):
    if i_string == "!help":
        print_help_help(i_medium, i_alias)

    elif i_string == "!aws":
        modules.connection.send_message("Usage: !aws asg <ASG> <Status/Desired Capacity>", i_medium, i_alias)
        modules.connection.send_message("Usage: !aws lambda <Function Name>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Issue AWS commands", i_medium, i_alias)

    elif i_string == "!calc":
        modules.connection.send_message("Usage: !calc <Operations>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Compute things faster than you", i_medium, i_alias)
            modules.connection.send_message("Tip: Functions available > https://docs.python.org/3/library/math.html", i_medium, i_alias)

    elif i_string == "!imdb":
        modules.connection.send_message("Usage: !imdb <Guessed Title>", i_medium, i_alias)
        modules.connection.send_message("Usage: !imdb <Guessed Title>#<Year>", i_medium, i_alias)
        modules.connection.send_message("Usage: !imdb id:<imdbID>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give information about a movie / TV serie", i_medium, i_alias)
            modules.connection.send_message("Tip: Title you enter is a guessed title, specify the year for more accuracy", i_medium, i_alias)

    elif i_string == "!meet":
        modules.connection.send_message("Usage: !meet <TimeZone> <HH:MM>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give the equivalence of the specified time input in several time zones", i_medium, i_alias)
            modules.connection.send_message("Tip: Valid time zones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones", i_medium, i_alias)

    elif i_string == "!money":
        modules.connection.send_message("Usage: !money <number> <CODE1>:<CODE2>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Convert an amount from one currency to another", i_medium, i_alias)
            modules.connection.send_message("Tip: Valid currency codes: https://en.wikipedia.org/wiki/ISO_4217", i_medium, i_alias)

    elif i_string == "!ping":
        modules.connection.send_message("Usage: !ping <optional_ip>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Make me ping either you or a given IP/DNS if possible", i_medium, i_alias)
            modules.connection.send_message("Tip: Works for IPv4 or IPv6", i_medium, i_alias)

    elif i_string == "!quit":
        modules.connection.send_message("Usage: !quit", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Make me quit IRC", i_medium, i_alias)
            modules.connection.send_message("Tip: Don't be mean please :'(", i_medium, i_alias)

    elif i_string == "!say":
        modules.connection.send_message("Usage: !say <something>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Make me speak!", i_medium, i_alias)
            modules.connection.send_message("Tip: Be smart and /msg me the command privately", i_medium, i_alias)

    elif i_string == "!steam":
        modules.connection.send_message("Usage: !steam <Game_Title>", i_medium, i_alias)
        modules.connection.send_message("Usage: !steam admin <Admin_Command>", i_medium, i_alias)
        modules.connection.send_message("Usage: !steam own <Player> <Game_Title>", i_medium, i_alias)
        modules.connection.send_message("Usage: !steam played <Game_Title>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Expose Steam information", i_medium, i_alias)

    elif i_string == "!time":
        modules.connection.send_message("Usage: !time <TimeZone>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give the time in the specified time zone", i_medium, i_alias)
            modules.connection.send_message("Tip: Get valid timezones of a country with: !time <two-letter-country-code>", i_medium, i_alias)
            modules.connection.send_message("---- Countries' codes: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2", i_medium, i_alias)

    elif i_string == "!yt":
        modules.connection.send_message("Usage: !yt <Display name or ID>", i_medium, i_alias)
        if mode == "detailed":
            modules.connection.send_message("Purpose: Give metadata about a YouTube Channel", i_medium, i_alias)
    else:
        print_help_help(i_medium, i_alias)
