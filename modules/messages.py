__author__ = 'Djidiouf'

# Project config
import config  # Parsed variables from command line


class Message:
    def __init__(self, channel):
        self.channel = channel

    def send_message(self, msg):
        """
        Transform a message in input into an encoded message send through IRC socket

        :param msg: string needed to be encoded and sent on IRC
        :return:
        """
        config.ircsock.send(bytes("PRIVMSG %s :" % self.channel + msg + "\r\n", "UTF-8"))
