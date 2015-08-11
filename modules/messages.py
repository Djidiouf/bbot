__author__ = 'Djidiouf'

# Python built-in modules
from datetime import datetime  # displaying date and time
import re  # REGEX compiler
import urllib.request  # Open url request on website
import json  # Library for being able to read Json file
import time  # anti flood if needed: time.sleep(2)
import os       # For instruction related to the OS
import shutil   # Used for OS tools

# Third-party modules
import pytz  # timezone information

# Project config
import config  # Parsed variables from command line


class Message:
    def __init__(self, channel):
        self.channel = channel

    # formatting needed for every message
    def send_message(self, msg):
        config.ircsock.send(bytes("PRIVMSG %s :" % self.channel + msg + "\r\n", "UTF-8"))

    def hello(self):
        self.send_message("Hello!")

    def give_time(self, tz_string):  # Responds to a user that inputs "!time Continent/City"
        # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

        tz = tz_string

        if tz == 'bchat':
            tz = 'Europe/London'
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
            tz = 'Europe/Stockholm'
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
            tz = 'Australia/Sydney'
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)
        else:
            tzinfo = pytz.timezone(tz)
            time_utc = datetime.now(tzinfo)
            self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tz)

    def give_hour_equivalence(self, i_string):  # Responds to an input as "!meet <Continent/City> <HH:MM>"
        # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        # /!\ currently only "utc" is working

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_string = i_string.partition(' ')
        tz = tuple_string[0]
        time_string = tuple_string[2]

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_time = time_string.partition(':')
        simple_hour = tuple_time[0]
        simple_minute = tuple_time[2]

        # hour and minute need to be int and not string
        hour = int(simple_hour)
        minute = int(simple_minute)

        tzinfo1 = pytz.timezone(tz)
        time_utc = datetime.now(tzinfo1)
        year = datetime.now(tzinfo1).year
        month = datetime.now(tzinfo1).month
        day = datetime.now(tzinfo1).day

        self.send_message(datetime(year, month, day, hour, minute, 0, 0, tzinfo1).strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo1)
        delta = datetime(year, month, day, hour, minute, 0, 0, tzinfo1) - time_utc
        # DEBUG self.send_message("Delta is: " + str(delta))

        tzinfo_london = pytz.timezone('Europe/London')
        time_utc = datetime.now(tzinfo_london) + delta
        self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_london)

        tzinfo_stockholm = pytz.timezone('Europe/Stockholm')
        time_utc = datetime.now(tzinfo_stockholm) + delta
        self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_stockholm)

        tzinfo_sydney = pytz.timezone('Australia/Sydney')
        time_utc = datetime.now(tzinfo_sydney) + delta
        self.send_message(time_utc.strftime('%Y-%m-%d - %H:%M:%S - %Z%z') + " - %s" % tzinfo_sydney)

    def money_rate(self, i_string):  # Responds to a user that inputs "!money <number> <CODE1>:<CODE2>"
        # https://www.google.com/finance/converter

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_string = i_string.partition(' ')
        amount = tuple_string[0]
        codes = tuple_string[2]

        # amount needs to be int and not string
        amount = float(amount)

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_time = codes.partition(':')
        code1 = tuple_time[0].upper()
        code2 = tuple_time[2].upper()

        url = 'https://www.google.com/finance/converter?a=1&from=%s&to=%s' % (code1, code2)

        # Define where the results could be find and convert the split separator in byte.
        # Can't be simplified as a variable can't be called through bytes
        separator1 = '</div>\n&nbsp;\n<div id=currency_converter_result>1 %s = <span class=bld>' % code1  # Google
        separator1 = str.encode(separator1)  # Convert it in a byte type

        separator2 = ' %s</span>' % code2  # Google
        separator2 = str.encode(separator2)  # Convert it in a byte type

        webpage = urllib.request.urlopen(url)

        rate = float(webpage.read().split(separator1)[1].split(separator2)[0].strip())
        self.send_message('Rate: 1 %s = %.4f %s' % (code1, rate, code2))

        total = amount * rate
        self.send_message('%.2f %s = %.2f %s' % (amount, code1, total, code2))
        webpage.close()

    def say(self, i_input):  # Responds to an input as "!say <something>"
        self.send_message(i_input)

    def steam_price(self, i_string):  # Responds to a user that inputs "!steamprice <Game Title>"
        # using Steam API: http://api.steampowered.com/ISteamApps/GetAppList/v0001/
        # using Steam API: http://store.steampowered.com/api/appdetails?appids=392400&cc=fr

        # Time variables
        now = time.time()
        age = 86400  # 86400 = 24hr

        # Condition variables
        title_found = False
        title_spelling = False

        # Steam API variables
        cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached
        country = "fr"
        appid_guess = 0

        # Results variables
        results_nb = 3  # Number of result which will be displayed if an exact natch didn't occur
        results = []


        nameguess= i_string

        if nameguess == "@rm-cache":
            shutil.rmtree(cache_steam_dir)
            self.send_message("Cache has been deleted")
            return  # Use ** return ** if in a function, exit() otherwise

        # Method ONLINE: URL only, no cache ----------------------
        # url_steam_appsid = request.urlopen('http://api.steampowered.com/ISteamApps/GetAppList/v0001/').read().decode('utf-8')
        # url_steam_appsid = urllib.request.urlopen('http://lib.openlog.it/steamapi.json').read().decode('utf-8')
        # steam_appsid = json.loads(url_steam_appsid)

        # Method CACHE: Retrieve and Store local file --------------
        if not os.path.exists(cache_steam_dir):  # Test if the directory exists
            os.makedirs(cache_steam_dir)
        steam_appsid_filename = os.path.join(cache_steam_dir, 'steam_appsid.json')  # Name of the local file

        # Download the file if it doesn't exist or is too old
        if not os.path.isfile(steam_appsid_filename) or os.stat(steam_appsid_filename).st_mtime < (now - age):
            self.send_message("Processing in progress (AppsID) ...")
            local_url_appsid = urllib.request.urlretrieve('http://api.steampowered.com/ISteamApps/GetAppList/v0001/', filename=steam_appsid_filename)
        with open(steam_appsid_filename, encoding="utf8") as steam_appsid_data:
            steam_appsid = json.load(steam_appsid_data)

        # print(url_appsid['applist']['apps']['app'])  # [{'name': 'Dedicated Server', 'appid': 5}, {'name': 'Steam Client', 'appid': 7}, {'name': 'winui2', 'appid': 8}, {'name': 'Counter-Strike', 'appid': 10}, {'name': 'Team Fortress Classic', 'appid': 20}, {'name': 'INK - Soundtrack + Art', 'appid': 392400}]
        # print(url_appsid['applist']['apps']['app'][2]['appid'])  # 8
        # print(url_appsid['applist']['apps']['app'][5]['name'])  # INK - Soundtrack + Art

        # Read the JSON data file
        for line in steam_appsid['applist']['apps']['app']:

            if line['name'] == nameguess:
                title_found = True
                title_spelling = False  # Need to set this one to False in case an approximative match had been made previously

                appid_guess = line['appid']
                appid_guess = str(appid_guess)
                break  # As an exact match has been found, there is no need to go further

            if line['name'].startswith(nameguess):
                title_spelling = True  # Found at least one approximative match
                results.append(line['name'])  # Add each match to a list

            # Close the file
            steam_appsid_data.close()

        if title_found == True:
            url_steam_appsmeta = 'http://store.steampowered.com/api/appdetails?appids=%s&cc=%s' % (appid_guess, country)
            # print(webpage)

            # Method ONLINE: URL only, no cache ----------------------
            # url_steam_appsmeta = urllib.request.urlopen(url_steam_appsmeta).read().decode('utf-8')
            # steam_appsmeta = json.loads(url_steam_appsmeta)

            # Method CACHE: Retrieve and Store local file --------------
            if not os.path.exists(cache_steam_dir):  # Test if the directory exists
                os.makedirs(cache_steam_dir)
            steam_appsmeta_filename = 'steam_appsmeta%s.json' % appid_guess
            steam_appsmeta_filename = os.path.join(cache_steam_dir, steam_appsmeta_filename)  # Name of the local file

            # Download the file if it doesn't exist or is too old
            if not os.path.isfile(steam_appsmeta_filename) or os.stat(steam_appsmeta_filename).st_mtime < (now - age):
                self.send_message("Processing in progress (%s) ..." % appid_guess)
                local_url_appsmeta = urllib.request.urlretrieve(url_steam_appsmeta, filename=steam_appsmeta_filename)
            with open(steam_appsmeta_filename, encoding="utf8") as steam_appsmeta_data:
                steam_appsmeta = json.load(steam_appsmeta_data)

            # Test of keys existence
            if "data" in steam_appsmeta[appid_guess]:
                if "price_overview" in steam_appsmeta[appid_guess]["data"]:
                    # print(steam_price[appid_guess]["data"]["price_overview"])  # complete price overview
                    price_initial = steam_appsmeta[appid_guess]["data"]["price_overview"]['initial']
                    price_discount = steam_appsmeta[appid_guess]["data"]["price_overview"]['discount_percent']
                    price_final = steam_appsmeta[appid_guess]["data"]["price_overview"]['final']
                    price_currency = steam_appsmeta[appid_guess]["data"]["price_overview"]['currency']

                    price_initial = float(price_initial)
                    price_initial *= 0.01  # Price was given in cents, switch to a more readable format
                    price_discount = int(price_discount)
                    price_final = float(price_final)
                    price_final *= 0.01  # Price was given in cents, switch to a more readable format

                    self.send_message("%s is at %.2f %s " % (nameguess, price_final, price_currency) + "(from: %.2f %s , discount: %i%%)" % (price_initial, price_currency, price_discount))
                else:
                    self.send_message("No price information for that title")

                if "about_the_game" in steam_appsmeta[appid_guess]["data"]:
                    price_about_the_game = steam_appsmeta[appid_guess]["data"]["about_the_game"]

                    # Substitute with nothing some html
                    price_about_the_game = re.sub("<br />", "", price_about_the_game)
                    price_about_the_game = re.sub("<strong>", "", price_about_the_game)
                    price_about_the_game = re.sub("</strong>", "", price_about_the_game)

                    self.send_message("About: %s" % price_about_the_game[0:130] + " [...]")

                if "metacritic" in steam_appsmeta[appid_guess]["data"]:
                    price_metacritic_score = steam_appsmeta[appid_guess]["data"]["metacritic"]["score"]
                    self.send_message("Metacritic: %s" % price_metacritic_score)
            else:
                self.send_message("No info available for that title")

            # Display the Steam Sore url of the title requested
            self.send_message("SteamStore: http://store.steampowered.com/app/%s?cc=fr" % appid_guess)

            # Close the file
            steam_appsmeta_data.close()

        if title_spelling == True:
            self.send_message("Exact title not found, you can try:")
            for item in results[:results_nb]:  # Display X first items
                self.send_message(item)

        if title_found == False and title_spelling == False:
            self.send_message("Title not found")
