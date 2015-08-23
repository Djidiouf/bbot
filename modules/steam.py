__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website
import urllib.request  # Open url request on website
import json  # Library for being able to read Json file
import time  # anti flood if needed: time.sleep(2)
import os       # For instruction related to the OS
import shutil   # Used for OS tools

# Project modules
import modules.textalteration
import modules.connection


def get_app_id(i_string):
    """
    :param i_string:
    :return:
    'Rust'  (True, ('252490', 'Rust'), ['Rusty Hearts', 'Rusty Hearts Meilin Starter Pack'))
    'Rus'   (False, (), ['Runaway, The Dream of The Turtle Trailer', 'RUSE Open Beta', 'Runaway: A Road Adventure'])
    'zwioq' (False, (), [])
    """
    # Main variables
    nameguess = i_string.lower()
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    # Time variables
    now = time.time()
    cache_age = 86400  # 86400 = 24hr
    m, s = divmod(cache_age, 60)
    h, m = divmod(m, 60)

    # Condition variables
    title_found = False

    # Results variables
    similar_titles = []
    tup_id = ()

    # Method CACHE: Retrieve and Store local file --------------
    if not os.path.exists(cache_steam_dir):  # Test if the directory exists
        os.makedirs(cache_steam_dir)
    steam_appsid_filename = os.path.join(cache_steam_dir, 'steam_appsid.json')  # Name of the local file

    # Download the file if it doesn't exist or is too old
    if not os.path.isfile(steam_appsid_filename) or os.stat(steam_appsid_filename).st_mtime < (now - cache_age):
        modules.connection.send_message("Cache outdated (> %dhr %02dmin), retrieving new Steam apps list ..." % (h, m))
        urllib.request.urlretrieve('http://api.steampowered.com/ISteamApps/GetAppList/v0001/', filename=steam_appsid_filename)
    with open(steam_appsid_filename, encoding="utf8") as f:
        steam_appsid = json.load(f)

    # Read the JSON data file
    for line in steam_appsid['applist']['apps']['app']:
        if line['name'].lower() == nameguess:
            title_found = True

            appid_guess = line['appid']
            appid_guess = str(appid_guess)
            nameguess = line['name']  # Ensure that the correct case is displayed in the future
            tup_id = appid_guess, nameguess

        if line['name'].lower().startswith(nameguess):
            similar_titles.append(line['name'])  # Add each match to a list

    result = title_found, tup_id, similar_titles
    return result


def get_app_metadata(steam_id, cc_code):
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    # Time variables
    now = time.time()
    cache_age = 86400  # 86400 = 24hr

    url_steam_appsmeta = 'http://store.steampowered.com/api/appdetails?appids=%s&cc=%s' % (steam_id, cc_code)

    # Method CACHE: Retrieve and Store local file --------------
    if not os.path.exists(cache_steam_dir):  # Test if the directory exists
        os.makedirs(cache_steam_dir)
    steam_appsmeta_filename = 'steam_appsmeta_%s.json' % steam_id
    steam_appsmeta_filename = os.path.join(cache_steam_dir, steam_appsmeta_filename)  # Name of the local file

    # Download the file if it doesn't exist or is too old
    if not os.path.isfile(steam_appsmeta_filename) or os.stat(steam_appsmeta_filename).st_mtime < (now - cache_age):
        modules.connection.send_message("Title found (%s), retrieving last metadata ..." % steam_id)
        urllib.request.urlretrieve(url_steam_appsmeta, filename=steam_appsmeta_filename)

    with open(steam_appsmeta_filename, encoding="utf8") as f:
        steam_appsmeta = json.load(f)

    return steam_appsmeta


def steam_price(i_string):
    """
    Responds to a user that inputs "!steamprice <Game Title>"
    using Steam API: http://api.steampowered.com/ISteamApps/GetAppList/v0001/
    using Steam API: http://store.steampowered.com/api/appdetails?appids=392400&cc=fr

    :param i_string: a string with these elements: "<Game Title>"
    :print: parsed answer about Steam title from the API
    """

    # Main variables
    nameguess = i_string.lower()
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    # Steam API variable
    country_currency = "fr"

    # Results variable
    results_nb = 3  # Number of result which will be displayed if an exact natch didn't occur

    # Clear Cache
    if nameguess == "@rm-cache":
        shutil.rmtree(cache_steam_dir)
        modules.connection.send_message("Cache has been deleted")
        return  # Use ** return ** if in a function, exit() otherwise

    # Retrieve all information, get: (True, ('252490', 'Rust'), ['Rusty Hearts', 'Rusty Hearts Meilin Starter'))
    whatweget = get_app_id(nameguess)

    if whatweget[0]:
        appid_guess = whatweget[1][0]
        corrected_name = whatweget[1][1]

        # Retrieve all metadata of a specified Steam app
        steam_appsmeta = get_app_metadata(appid_guess, country_currency)

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

                modules.connection.send_message("%s is at %.2f %s " % (corrected_name, price_final, price_currency) + "(from: %.2f %s , discount: %i%%)" % (price_initial, price_currency, price_discount))
            else:
                modules.connection.send_message("No price information for that title")

            if "about_the_game" in steam_appsmeta[appid_guess]["data"]:
                price_about_the_game = steam_appsmeta[appid_guess]["data"]["about_the_game"]

                # Substitute with nothing some html
                html_elements = ["<p>", "<br />", "<strong>", "</strong>", "<i>", "</i>"]
                price_about_the_game = modules.textalteration.string_cleanup(price_about_the_game, html_elements)

                modules.connection.send_message("About: %s" % price_about_the_game[0:130] + " [...]")

            if "metacritic" in steam_appsmeta[appid_guess]["data"]:
                price_metacritic_score = steam_appsmeta[appid_guess]["data"]["metacritic"]["score"]
                modules.connection.send_message("Metacritic: %s" % price_metacritic_score)
        else:
            modules.connection.send_message("No info available for that title")

        # Display the Steam Store url of the title requested
        modules.connection.send_message("SteamStore: http://store.steampowered.com/app/%s?cc=fr" % appid_guess)

    elif not whatweget[0] and whatweget[2]:
        modules.connection.send_message("Exact title not found, you can try:")
        for item in whatweget[2][:results_nb]:  # Display <results_nb> first items
            modules.connection.send_message(item)

    else:
        modules.connection.send_message("Title not found")
