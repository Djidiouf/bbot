# bbot
bbot is an advanced IRC bot with fancy answers and features


## Installation
Platforms: Windows, MacOSX, Linux

Prerequisite: [Python 3.4](https://www.python.org/), pytz library (````pip install pytz````)

Download bbot by clicking on [Download ZIP](https://github.com/Djidiouf/bbot/archive/master.zip), or do a git clone.

Extract the bbot folder on your desktop and open a command line terminal (Windows: shift + right click on your desktop and do 'Open command window here').

    $ cd bbot

Rename the config_example.cfg to config.cfg and change these 5 variables under [bot_configuration]:

    server = your.irc.server.com
    channel = ##your_channel
    botnick = bbot
    port = 6697
    admins = You,Him

Launch the bbot with:

    $ python bbot.py


## Features

#### Hello <bbot>

    Someone: Hello <bbot>
    TheBot : Hello!


#### !aws asg
````!aws asg <ASG> <Status/Desired Capacity>"```` Bring up and down an AutoHeal instance.

Prerequisites: You must have configured the ASG alias in the configuration file in [aws][YourAlias] and be in [aws][allowed_users]. In addition, it's your responsability to set and secure your credentials. If you run this bot on an EC2 machine, set an IAM role instead of storing some credentials on your instance.

    Someone: !aws asg teamspeak 0
    TheBot : SuperTeamspeak-ASG is being shutdown

##### Variations and dry examples
    Someone: !aws asg teamspeak up
    Someone: !aws asg teamspeak down
    Someone: !aws asg teamspeak off


#### !calc
````!calc <Operations>```` Compute things faster than you. Available Math functions: https://docs.python.org/3/library/math.html

    Someone: !calc 52^12 * 5
    TheBot : 52^12 * 5 = 8.000000

    
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


#### !meet
````!meet <time_zone> <HH:MM>```` or ````!meet <HH:MM> <time_zone>```` Allow to see one <time_zone> given in specific timezones

    Someone: !meet utc 10:00
    TheBot : 10:00:00 - UTC
    TheBot : 11:00:00 - Europe/London
    TheBot : 12:00:00 - Europe/Oslo
    TheBot : 20:00:00 - Australia/Sydney


#### !ping
````!ping <optional_ip>```` Make TheBot ping either you (if not IP has been mentioned) or a given IP/DNS if possible

    Someone: !ping
    TheBot : Reply from 119.63.220.121: bytes=32 time=1ms TTL=64
    TheBot : Reply from 119.63.220.121: bytes=32 time=6ms TTL=64
    TheBot : Reply from 119.63.220.121: bytes=32 time<1ms TTL=64
    TheBot : Reply from 119.63.220.121: bytes=32 time=1ms TTL=64
    TheBot :     Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
    TheBot :     Minimum = 0ms, Maximum = 6ms, Average = 2ms
    
##### Variations and dry examples
    Someone: !ping 8.8.8.8
    Someone: !ping google.com
    Someone: !ping 2001:4860:4860::8888
    
NB, the capacity of pinging IPv6 is dependant on your server and network configuration.


#### !money
````!money <amount> <CODE1>:<CODE2>```` Convert an amount from one currency to another

    Someone: !money 15.5 EUR:AUD
    TheBot : 15.50 EUR = 23.09 AUD (1 EUR = 1.4894 AUD)

##### Variations and dry examples
    Someone: !money 28 EUR AUD
    Someone: !money 0.5 eur in AUD


#### !quit
````!quit```` Make the bot quit IRC NB: You must be an admin for this. this can be set in the config file at [bot_configuration][admins]

    Someone: !quit
    TheBot : *rires*
    
    Admin  : !quit
    TheBot (~TheBot@85.12.35.251) has quit IRC (Remote host closed  the connection)
    
    
#### !say
````!say <text>```` Allow you to make the bbot speaks! NB: You can send that command in private

    Someone: !say I'm the best bbot
    TheBot : I'm the best bbot
    
    
#### !steam
````!steam <Title>```` Retrieve data info about a specific Title.

    Someone: !steam Cities: Skylines
    TheBot : Cities: Skylines — Metacritic: 85
    TheBot : Steam: 27.99€ — http://store.steampowered.com/app/255710
    TheBot : AKS: 3.73€ — http://www.allkeyshop.com/blog/buy-cities-in-motion-cd-key-compare-prices/
    TheBot : About: Cities: Skylines is a modern take on the classic city simulation. The game introduces new game play elements to realize the thrill and hardships of creating and maintaining a real city whilst expanding on some well-established tropes of the city building experience. From the makers of the Cities in Motion franchise, the game boasts a fully realized  [...]
    TheBot : Owned by: ARRG (60h07min), Djidiouf (69h57min), Timst (9h12min)

````!steam <Title>```` If an exact match hasn't been found, 3 potential results will be displayed.

    Someone: !steam PAYDAY
    TheBot : Exact title not found, you can try:
    TheBot : PAYDAY: The Heist
    TheBot : PAYDAY The Heist Mercy Hospital Trailer
    TheBot : PAYDAY: The Heist - Wolfpack Weapons


#### !steam admin
````!steam admin rm-cache```` Delete the cache folder for steam files: "cache-steam"

    Someone: !steam admin rm-cache
    TheBot : Cache has been deleted


#### !steam own
````!steam own <Player> <Title>```` Tell if a player owns a specific title

    Someone: !steam own djidiouf Planetary Annihilation
    TheBot : Djidiouf has played Planetary Annihilation for 36h 53min

````!steam own <Player> <Title>```` If an exact match hasn't been found, 3 potential results will be displayed.

    Someone: !steam own Djidiouf Planetary
    TheBot : Exact title not found, you can try:
    TheBot : Planetary Annihilation
    TheBot : Planetary Annihilation - Digital Deluxe Bundle
    TheBot : Planetary Annihilation - Original Soundtrack

    
#### !steam played
````!steam played <Game_Title>```` Report playtime for each person mentioned in the config file at [steam][owners]

    Someone: !steam played Factorio
    TheBot : Owned by: ARRG (137h05min), Timst (33h25min)
    
    
#### !steam spy
````!steam spy <Player>```` Report every game played by a specific player for the last 2 weeks

    Someone: !steam spy Timst
    TheBot : In the last 2 weeks Timst has played:
    TheBot : NEO Scavenger (1h00min)
    TheBot : The Flame in the Flood (5h16min)
    TheBot : Cossacks 3 (0h34min)
    TheBot : Guild of Dungeoneering (2h35min)
    TheBot : Streets of Rogue (0h45min)
    TheBot : Endless Legend™ (5h54min)
    TheBot : PLAYERUNKNOWN'S BATTLEGROUNDS (6h14min)
    TheBot : -- For a total of 22h18min (average of 1h35min per day)

    
#### !time
````!time <time_zone>```` Give time of timezone in https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

    Someone: !time Australia/Sydney
    TheBot : 2015-08-05 - 10:28:04 - AEST+1000 - Australia/Sydney

````!time bchat```` Special command that you can change in order to give you specific timezones at once

    Someone: !time bchat
    TheBot : 01:28:25 - Europe/London
    TheBot : 02:28:25 - Europe/Oslo
    TheBot : 10:28:25 - Australia/Sydney
    
    
#### !yt
````!yt <Display name or ID>```` Give metadata about a YouTube Channel

    Someone: !yt groink groink
    TheBot : Videos: 617 - Views: 92912 - Subs: 813
    TheBot : Channel: https://www.youtube.com/channel/UCc3d42oqhgYgFGL0e2rR-gQ
    

### Version
0.1


### Tech
bbot is made in:

* Python - 3.6.1


### Development
Want to contribute? Great! But don't do it now, wait for the Release.


### Todo's
* more features
* other things


### License
Something
