# bbot
bbot is an advanced IRC bot with fancy answers and features


## Installation
Platforms: Windows, MacOSX, Linux

Prerequisite: [Python 3.4](https://www.python.org/), pytz library (````pip install pytz````)

Download bbot by clicking on [Download ZIP](https://github.com/Djidiouf/bbot/archive/master.zip), or do a git clone.

Extract the bbot folder on your desktop and open a command line terminal (Windows: shift + right click on your desktop and do 'Open command window here').

    $ cd bbot
    $ python bbot.py

Rename the config_example.cfg to config.cfg and change these 5 variables under [bot_configuration]:

    server = your.irc.server.com
    channel = ##your_channel
    botnick = bbot
    port = 6667
    admins = You,Him


### Features

#### Hello <bbot>

    Someone: Hello <bbot>
    TheBot : Hello!


#### !say
````!say <text>```` Allow you to make the bbot speaks! NB: You can send that command in private

    Someone: !say I'm the best bbot
    TheBot : I'm the best bbot


#### !time
````!time <time_zone>```` Give time of timezone in https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    Someone: !time Australia/Sydney
    TheBot : 2015-08-05 - 10:28:04 - AEST+1000 - Australia/Sydney

````!time bchat```` Special command that you can change in order to give you specific timezones at once

    Someone: !time bchat
    TheBot : 2015-08-05 - 01:28:25 - BST+0100 - Europe/London
    TheBot : 2015-08-05 - 02:28:25 - CEST+0200 - Europe/Stockholm
    TheBot : 2015-08-05 - 10:28:25 - AEST+1000 - Australia/Sydney


#### !meet
````!meet <time_zone> <HH:MM>```` Allow to see one <time_zone> given in specific timezones

    Someone: !meet utc 10:00
    TheBot : 2015-08-06 - 10:00:00 - UTC+0000 - UTC
    TheBot : 2015-08-06 - 11:00:00 - BST+0100 - Europe/London
    TheBot : 2015-08-06 - 12:00:00 - CEST+0200 - Europe/Oslo
    TheBot : 2015-08-06 - 20:00:00 - AEST+1000 - Australia/Sydney


#### !money
````!money <amount> <CODE1>:<CODE2>```` Convert an amount from one currency to another

    Someone: !money 15.5 EUR:AUD
    TheBot : 15.50 EUR = 23.09 AUD (1 EUR = 1.4894 AUD)


#### !steamown
````!steamown <Player> <Title>```` Tell if a player owns a specific title

    Someone: !steamown djidiouf Planetary Annihilation
    TheBot : djidiouf owns Planetary Annihilation and has played for 36hr 19min

````!steamown <Player> <Title>```` If an exact match hasn't been found, 3 potential results will be displayed.

    Someone: !steamown Djidiouf Planetary
    TheBot : Exact title not found, you can try:
    TheBot : Planetary Annihilation
    TheBot : Planetary Annihilation - Digital Deluxe Bundle
    TheBot : Planetary Annihilation - Original Soundtrack


#### !steamprice
````!steamprice <Title>```` Retrieve data info about a specific Title.

    Someone: !steamprice Cities: Skylines
    TheBot : Data outdated (> 24hr 00min), retrieving new Steam titles list ...
    TheBot : Title found (255710), retrieving last metadata ...
    TheBot : Cities: Skylines is at 27.99 EUR (from: 27.99 EUR , discount: 0%)
    TheBot : About: Cities: Skylines is a modern take on the classic city simulation. The game introduces new game play elements to realize the thrill [...]
    TheBot : Metacritic: 86
    TheBot : SteamStore: http://store.steampowered.com/app/255710?cc=fr

````!steamprice <Title>```` If an exact match hasn't been found, 3 potential results will be displayed.

    Someone: !steamprice PAYDAY
    TheBot : Exact title not found, you can try:
    TheBot : PAYDAY: The Heist
    TheBot : PAYDAY The Heist Mercy Hospital Trailer
    TheBot : PAYDAY: The Heist - Wolfpack Weapons
    
````!steamprice @rm-cache```` Delete the cache folder for steam files: "cache-steam"

    Someone: !steamprice @rm-cache
    TheBot : Cache has been deleted
    

#### !imdb
````!imdb <Guessed Title>```` Retrieve data info about a movie / TV show.

    Someone: !imdb My name is Nobody
    TheBot : Title: My Name Is Nobody (Release date: 17 Jul 1974)
    TheBot : Italy, France, West Germany - 116 min - Western, Comedy
    TheBot : Plot: A young, easygoing gunman (Hill) worships and competes with an old gunfighter (Fonda) who only wants to retire.imdbID: tt0070215 - Rating: 7.5

````!imdb <Guessed Title>#<Year>```` Retrieve data info about a movie / TV show.

    Someone: !imdb lost#2004
    TheBot : Title: Lost (Release date: 22 Sep 2004)
    TheBot : USA - 44 min - Adventure, Drama, Fantasy
    TheBot : Plot: The survivors of a plane crash are forced to work together in order to survive on a seemingly deserted tropical island.
    TheBot : imdbID: tt0411008 - Rating: 8.5

````!imdb id:<imdbID>```` Retrieve data info about a movie / TV show.

    Someone: !imdb id:tt0386676
    TheBot : Title: The Office (Release date: 24 Mar 2005)
    TheBot : USA - 22 min - Comedy
    TheBot : Plot: A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium. Based on the hit BBC series.
    TheBot : imdbID: tt0386676 - Rating: 8.8


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
