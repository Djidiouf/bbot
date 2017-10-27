__author__ = 'Djidiouf'

# Project modules
import modules.connection


def hello():
    """
    Say hello to people when they say Hello <bbot>
    :return:
    """
    modules.connection.send_message("Hello!")

def main(i_input, i_medium, i_alias=None):
    """
    Responds to an input as "!say <something>"
    :param i_input: whatever people want the bot to say
    :return:
    """
    modules.connection.send_message(i_input)
