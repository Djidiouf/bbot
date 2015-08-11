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

!meet utc <HH:MM> - Allow to see the specified UTC time given in specific timezones
```
Someone: !meet utc 10:00
TheBot : 2015-08-06 - 10:00:00 - UTC+0000 - UTC
TheBot : 2015-08-06 - 11:00:00 - BST+0100 - Europe/London
TheBot : 2015-08-06 - 12:00:00 - CEST+0200 - Europe/Stockholm
TheBot : 2015-08-06 - 20:00:00 - AEST+1000 - Australia/Sydney
```

!money <amount> <CODE1>:<CODE2> - Convert an amount from one currency to another
```
Someone: !money 15.5 EUR:AUD
TheBot : Rate: 1 EUR = 1.4894 AUD
TheBot : 15.50 EUR = 23.09 AUD
```

!steamprice <Title> - Retrieve data info about a specific Title. If an exact match hasn't been found, 3 potential results will be displayed.
```
Someone: !steamprice PAYDAY
TheBot : Exact title not found, you can try:
TheBot : PAYDAY: The Heist
TheBot : PAYDAY The Heist Mercy Hospital Trailer
TheBot : PAYDAY: The Heist - Wolfpack Weapons
```
```
Someone: !steamprice Cities:Skylines
TheBot : Cities: Skylines is at 27.99 EUR (from: 27.99 EUR , discount: 0%)
TheBot : About: Cities: Skylines is a modern take on the classic city simulation. The game introduces new game play elements to realize the thrill and hardships of cr [...]
TheBot : Metacritic: 86
TheBot : SteamStore: http://store.steampowered.com/app/255710?cc=fr
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
