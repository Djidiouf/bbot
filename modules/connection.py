__author__ = 'Djidiouf'

import socket
import configparser
import ssl
import os


def send_message(i_msg, i_medium=None, i_alias=None):
        """
        Transform a message in input into an encoded message send through IRC socket

        :param i_msg: string needed to be encoded and sent on IRC
        :param i_medium: channel or private
        :param i_alias: receiver of the message if any
        :return:
        """
        botnick = config['bot_configuration']['botnick']
        channel = config['bot_configuration']['channel']

        if i_medium == botnick:
            ircsock.send(bytes("PRIVMSG %s :" % i_alias + i_msg + "\r\n", "UTF-8"))
        else:
            ircsock.send(bytes("PRIVMSG %s :" % channel + i_msg + "\r\n", "UTF-8"))


def ping():  # Respond to server pings
    ircsock.send(bytes("PONG :Pong\n", "UTF-8"))


def join_chan(i_chan):  # Join channel
    ircsock.send(bytes("JOIN %s\r\n" % i_chan, "UTF-8"))


def receive_data():
    a = ircsock.recv(2048)  # receive data from the server
    return a


# list of SSL ports for IRC
irc_ssl_ports = [6697, 7070]

# Parsing config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
server = config['bot_configuration']['server']
channel = config['bot_configuration']['channel']
botnick = config['bot_configuration']['botnick']
port = int(config['bot_configuration']['port'])

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
