__author__ = 'Djidiouf'

# Python built-in modules
import configparser
import os
import sys

# Third-party modules

# Project modules
import modules.connection


def main(i_string, i_medium, i_alias=None):

    print("i_string : " + i_string)
    print("i_medium : " + i_medium)
    print("i_alias : " + i_alias)

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    admins_list = config['bot_configuration']['admins'].split(",")

    if i_alias:
        if i_alias in admins_list:
            modules.connection.send_message("Bye bye bitches!")
            sys.exit("Bot admin requested a shutdown.")
        else:
            modules.connection.send_message("*rires*", i_medium, i_alias)
    else:
        modules.connection.send_message("*rires*", i_medium, i_alias)
