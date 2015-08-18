__author__ = 'Djidiouf'

import socket
import configparser
import ssl

# list of SSL ports for IRC
irc_ssl_ports = [6697, 7070]


def send_message(msg):
        """
        Transform a message in input into an encoded message send through IRC socket

        :param msg: string needed to be encoded and sent on IRC
        :return:
        """
        chan = config.get('bot_configuration', 'channel')
        ircsock.send(bytes("PRIVMSG %s :" % chan + msg + "\r\n", "UTF-8"))


def ping():  # Respond to server pings
    ircsock.send(bytes("PONG :Pong\n", "UTF-8"))


def join_chan(chan):  # Join channel
    ircsock.send(bytes("JOIN %s\r\n" % chan, "UTF-8"))


def receive_data():
    a = ircsock.recv(2048)  # receive data from the server
    return a


config = configparser.RawConfigParser()
config.read('config.cfg')
server = config.get('bot_configuration', 'server')
channel = config.get('bot_configuration', 'channel')
botnick = config.get('bot_configuration', 'botnick')
port = config.getint('bot_configuration', 'port')

# connection --------------------------------------------------------------------
# connect to the server
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Determine if an SSL connection can be attempted if a IRC SSL port is configured
if port in irc_ssl_ports:
    ircsock = ssl.wrap_socket(ircsock)

ircsock.connect((server, port))  # Connect to configured port

# Sends the username, real name etc : user authentication
ircsock.send(bytes("USER %s %s %s :%s\r\n" % (botnick, botnick, botnick, botnick), "UTF-8"))

# Assignment of a nick to the bot
ircsock.send(bytes("NICK %s\r\n" % botnick, "UTF-8"))
