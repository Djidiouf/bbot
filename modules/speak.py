__author__ = 'Djidiouf'

# Project modules
import modules.messages
import config


def hello():
    """
    Say hello to people when they say Hello <bbot>
    :return:
    """
    modules.messages.Message(config.channel).send_message("Hello!")

def say(i_input):
    """
    Responds to an input as "!say <something>"
    :param i_input: whatever people want the bot to say
    :return:
    """
    modules.messages.Message(config.channel).send_message(i_input)
