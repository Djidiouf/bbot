# -------------------------------------------------------------------------------
# Name:         bbot
# Purpose:      a bot without limits
#
# Author:       Djidiouf
#
# Created:      2015-07-23
# Licence:      bchat-licence
# -------------------------------------------------------------------------------

# Import socket library
import socket
# Import argument library
import argparse

from datetime import datetime

# functions ---------------------------------------------------------------------
# functions that will do the handling of the servers's data


def ping():  # Respond to server pings
    ircsock.send(bytes("PONG :Pong\n", "UTF-8"))


def join_chan(chan):  # Join channel
    ircsock.send(bytes("JOIN %s\r\n" % chan, "UTF-8"))


def hello():  # Responds to a user that inputs "Hello <botname>"
    ircsock.send(bytes("PRIVMSG %s :Hello \r\n" % args.channel, "UTF-8"))


def give_time():  # Responds to a user that inputs "Hello <botname>"
    ircsock.send(bytes("PRIVMSG %s :Time is " % args.channel + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\r\n", "UTF-8"))

# arguments ---------------------------------------------------------------------
parser = argparse.ArgumentParser(description='bbot, a bot without limits')
parser.add_argument("-s", "--server", help="Server name", required=True)
parser.add_argument("-c", "--channel", help="Channel name", required=True)
parser.add_argument("-b", "--botnick", help="bbot nickname", required=True)
args = parser.parse_args()


# connection --------------------------------------------------------------------
# connect and join the configured channel
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((args.server, 6667))  # Connect to port 6667

# Sends the username, real name etc : user authentication
ircsock.send(bytes("USER %s %s %s :%s\r\n" % (args.botnick, args.botnick, args.botnick, args.botnick), "UTF-8"))

# Assignment of a nick to the bot
ircsock.send(bytes("NICK %s\r\n" % args.botnick, "UTF-8"))

# After connection, oin the specified channel
join_chan(args.channel)


# data reception ---------------------------------------------------------------
# Receive all the data from the server & channel
while 1:  # infinite loop
    ircmsg = ircsock.recv(2048)  # receive data from the server
    ircmsg = ircmsg.strip(bytes("\n\r", "UTF-8"))  # removes unnecessary linebreaks
    print(ircmsg)  # DEBUG: print output of the channel

    # tracks PING : if the server pings the bot, it will answer
    if ircmsg.find(bytes("PING :", "UTF-8")) != -1:
        ping()

    # tracks "Hello <botname> <any message>"
    if ircmsg.find(bytes(":Hello %s" % args.botnick, "UTF-8")) != -1:
        hello()

    # tracks "Hello <botname> <any message>"
    if ircmsg.find(bytes(":!time", "UTF-8")) != -1:
        give_time()
