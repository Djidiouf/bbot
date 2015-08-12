__author__ = 'Djidiouf'

# Project config
import config  # Parsed variables from command line


class Message:
    def __init__(self, channel):
        self.channel = channel

    # formatting needed for every message
    def send_message(self, msg):
        config.ircsock.send(bytes("PRIVMSG %s :" % self.channel + msg + "\r\n", "UTF-8"))

    def hello(self):
        self.send_message("Hello!")

    def say(self, i_input):  # Responds to an input as "!say <something>"
        self.send_message(i_input)
