__author__ = 'Djidiouf'

import socket
import config


def send_message(msg):
        """
        Transform a message in input into an encoded message send through IRC socket

        :param msg: string needed to be encoded and sent on IRC
        :return:
        """
        ircsock.send(bytes("PRIVMSG %s :" % config.channel + msg + "\r\n", "UTF-8"))


def ping():  # Respond to server pings
    ircsock.send(bytes("PONG :Pong\n", "UTF-8"))


def join_chan(chan):  # Join channel
    ircsock.send(bytes("JOIN %s\r\n" % chan, "UTF-8"))


def receive_data():
    a = ircsock.recv(2048)  # receive data from the server
    return a


# connection --------------------------------------------------------------------
# connect and join the configured channel
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((config.server, 6667))  # Connect to port 6667

# Sends the username, real name etc : user authentication
ircsock.send(bytes("USER %s %s %s :%s\r\n" % (config.botnick, config.botnick, config.botnick, config.botnick), "UTF-8"))

# Assignment of a nick to the bot
ircsock.send(bytes("NICK %s\r\n" % config.botnick, "UTF-8"))

# After connection, join the specified channel
# join_chan(config.channel)
