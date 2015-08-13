__author__ = 'Djidiouf'

import socket
import configparser


def send_message(msg):
        """
        Transform a message in input into an encoded message send through IRC socket

        :param msg: string needed to be encoded and sent on IRC
        :return:
        """
        channel = conf.get('bot_configuration', 'channel')
        ircsock.send(bytes("PRIVMSG %s :" % channel + msg + "\r\n", "UTF-8"))


def ping():  # Respond to server pings
    ircsock.send(bytes("PONG :Pong\n", "UTF-8"))


def join_chan(chan):  # Join channel
    ircsock.send(bytes("JOIN %s\r\n" % chan, "UTF-8"))


def receive_data():
    a = ircsock.recv(2048)  # receive data from the server
    return a


conf = configparser.RawConfigParser()
conf.read('config.cfg')
server = conf.get('bot_configuration', 'server')
channel = conf.get('bot_configuration', 'channel')
botnick = conf.get('bot_configuration', 'botnick')
port = conf.getint('bot_configuration', 'port')

# connection --------------------------------------------------------------------
# connect to the server
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port))  # Connect to configured port

# Sends the username, real name etc : user authentication
ircsock.send(bytes("USER %s %s %s :%s\r\n" % (botnick, botnick, botnick, botnick), "UTF-8"))

# Assignment of a nick to the bot
ircsock.send(bytes("NICK %s\r\n" % botnick, "UTF-8"))
