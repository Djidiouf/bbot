# bbot
bbot is an advanced IRC bot with fancy answers and features

## Installation
Platforms: Windows, MacOSX, Linux

Prerequisite: [Python 3.4](https://www.python.org/)

Download bbot by clicking on [Download ZIP](https://github.com/Djidiouf/bbot/archive/master.zip), or do a git clone.

Extract the bbot folder on your desktop and open a command line terminal (Windows: shift + right click on your desktop and do 'Open command window here').

```sh
$ cd bbot
$ python bbot.py -s <SERVER>  -c <CHANNEL> -b <BOTNICKNAME>
```

Example
```
python bbot.py -s irc.freenode.net  -c ##rimbatou -b bbot
```

The channel name can be put between quotes if needed.

Example
```
python bbot.py -s irc.freenode.net  -c "##rimbatou" -b bbot
```

### Features

Hello <bbot>
```
Someone: Hello <bbot>
TheBot : Hello!
```

!time <time_zone> - Give time of timezone in https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
```
Someone: !time Australia/Sydney
TheBot : 2015-08-05 - 10:28:04 - AEST+1000 - Australia/Sydney
```

!time bchat - Special command that you can change in order to give you specific timezones at once
```
Someone: !time bchat
TheBot : 2015-08-05 - 01:28:25 - BST+0100 - Europe/London
TheBot : 2015-08-05 - 02:28:25 - CEST+0200 - Europe/Stockholm
TheBot : 2015-08-05 - 10:28:25 - AEST+1000 - Australia/Sydney
```

### Version
0.1

### Tech
bbot is made in:

* Python - 3.4.3

### Development
Want to contribute? Great! But don't do it now, wait for the Release.


### Todo's
* more features
* other things

### License
Something
