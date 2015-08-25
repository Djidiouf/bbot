__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website
import urllib.request  # Open url request on website
import json  # Library for being able to read Json file
import time  # anti flood if needed: time.sleep(2)
import os       # For instruction related to the OS
import shutil   # Used for OS tools
import configparser

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
    title_requested = i_string.lower()
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
        if line['name'].lower() == title_requested:
            title_found = True

            steam_app_id = line['appid']
            steam_app_id = str(steam_app_id)
            title_corrected = line['name']  # Ensure that the correct case is displayed in the future
            tup_id = steam_app_id, title_corrected

        if line['name'].lower().startswith(title_requested):
            similar_titles.append(line['name'])  # Add each match to a list

    result = title_found, tup_id, similar_titles
    return result


def get_player_id(i_string, steam_api_key):
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    # Time variables
    now = time.time()
    cache_age = 86400  # 86400 = 24hr

    url_steam_player_meta = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=%s&vanityurl=%s' % (steam_api_key, i_string)

    # Method CACHE: Retrieve and Store local file --------------
    if not os.path.exists(cache_steam_dir):  # Test if the directory exists
        os.makedirs(cache_steam_dir)
    steam_player_id_filename = 'steam_player_id_%s.json' % i_string
    steam_player_id_filename = os.path.join(cache_steam_dir, steam_player_id_filename)  # Name of the local file

    # Download the file if it doesn't exist or is too old
    if not os.path.isfile(steam_player_id_filename) or os.stat(steam_player_id_filename).st_mtime < (now - cache_age):
        modules.connection.send_message("Retrieving ID for player %s ..." % i_string)
        urllib.request.urlretrieve(url_steam_player_meta, filename=steam_player_id_filename)

    with open(steam_player_id_filename, encoding="utf8") as f:
        steam_player_id = json.load(f)

    if "steamid" in steam_player_id["response"]:
        player_id = steam_player_id["response"]["steamid"]
        return player_id
    else:
        modules.connection.send_message("ID not found for player %s" % i_string)
        return

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


def get_owned_games(player_id, steam_api_key):
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    # Time variables
    now = time.time()
    cache_age = 86400  # 86400 = 24hr

    url_steam_player_meta = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&format=json' % (steam_api_key, player_id)

    # Method CACHE: Retrieve and Store local file --------------
    if not os.path.exists(cache_steam_dir):  # Test if the directory exists
        os.makedirs(cache_steam_dir)
    steam_player_meta_filename = 'steam_player_meta_%s.json' % player_id
    steam_player_meta_filename = os.path.join(cache_steam_dir, steam_player_meta_filename)  # Name of the local file

    # Download the file if it doesn't exist or is too old
    if not os.path.isfile(steam_player_meta_filename) or os.stat(steam_player_meta_filename).st_mtime < (now - cache_age):
        modules.connection.send_message("Player found (%s), retrieving last metadata ..." % player_id)
        urllib.request.urlretrieve(url_steam_player_meta, filename=steam_player_meta_filename)

    with open(steam_player_meta_filename, encoding="utf8") as f:
        steam_player_meta = json.load(f)

    return steam_player_meta


def steam_price(i_string):
    """
    Responds to a user that inputs "!steamprice <Game Title>"
    using Steam API: http://api.steampowered.com/ISteamApps/GetAppList/v0001/
    using Steam API: http://store.steampowered.com/api/appdetails?appids=392400&cc=fr

    :param i_string: a string with these elements: "<Game Title>"
    :print: parsed answer about Steam title from the API
    """

    # Main variables
    title_requested = i_string.lower()
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    # Steam API variable
    country_currency = "fr"

    # Results variable
    results_nb = 3  # Number of result which will be displayed if an exact natch didn't occur

    # Clear Cache
    if title_requested == "@rm-cache":
        shutil.rmtree(cache_steam_dir)
        modules.connection.send_message("Cache has been deleted")
        return  # Use ** return ** if in a function, exit() otherwise

    # Retrieve all information, get: (True, ('252490', 'Rust'), ['Rusty Hearts', 'Rusty Hearts Meilin Starter'))
    app_id_details = get_app_id(title_requested)
    is_steamapp_found = app_id_details[0]

    if is_steamapp_found:
        steam_app_id = app_id_details[1][0]
        title_corrected = app_id_details[1][1]

        # Retrieve all metadata of a specified Steam app
        steam_appsmeta = get_app_metadata(steam_app_id, country_currency)

        # Test of keys existence
        if "data" in steam_appsmeta[steam_app_id]:
            if "price_overview" in steam_appsmeta[steam_app_id]["data"]:
                # print(steam_price[steam_app_id]["data"]["price_overview"])  # complete price overview
                price_initial = steam_appsmeta[steam_app_id]["data"]["price_overview"]['initial']
                price_discount = steam_appsmeta[steam_app_id]["data"]["price_overview"]['discount_percent']
                price_final = steam_appsmeta[steam_app_id]["data"]["price_overview"]['final']
                price_currency = steam_appsmeta[steam_app_id]["data"]["price_overview"]['currency']

                price_initial = float(price_initial)
                price_initial *= 0.01  # Price was given in cents, switch to a more readable format
                price_discount = int(price_discount)
                price_final = float(price_final)
                price_final *= 0.01  # Price was given in cents, switch to a more readable format

                modules.connection.send_message("%s is at %.2f %s " % (title_corrected, price_final, price_currency) + "(from: %.2f %s , discount: %i%%)" % (price_initial, price_currency, price_discount))
            else:
                modules.connection.send_message("No price information for that title")

            if "about_the_game" in steam_appsmeta[steam_app_id]["data"]:
                price_about_the_game = steam_appsmeta[steam_app_id]["data"]["about_the_game"]

                # Substitute with nothing some html
                html_elements = ["<p>", "<br />", "<strong>", "</strong>", "<i>", "</i>"]
                price_about_the_game = modules.textalteration.string_cleanup(price_about_the_game, html_elements)

                modules.connection.send_message("About: %s" % price_about_the_game[0:130] + " [...]")

            if "metacritic" in steam_appsmeta[steam_app_id]["data"]:
                price_metacritic_score = steam_appsmeta[steam_app_id]["data"]["metacritic"]["score"]
                modules.connection.send_message("Metacritic: %s" % price_metacritic_score)
        else:
            modules.connection.send_message("No info available for that title")

        # Display the Steam Store url of the title requested
        modules.connection.send_message("SteamStore: http://store.steampowered.com/app/%s?cc=fr" % steam_app_id)

    elif not is_steamapp_found and app_id_details[2]:
        modules.connection.send_message("Exact title not found, you can try:")
        for item in app_id_details[2][:results_nb]:  # Display <results_nb> first items
            modules.connection.send_message(item)

    else:
        modules.connection.send_message("Title not found")


def player_owns_game(i_string):
    tuple_string = i_string.partition(' ')
    player_name = tuple_string[0]
    title_requested = tuple_string[2]

    game_found = False
    results_nb = 3

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    steam_api_key = config['API_keys']['steam']

    # Retrieve player ID
    player_id_details = get_player_id(player_name, steam_api_key)
    if player_id_details is None:
        return

    # Retrieve steam app ID
    app_id_details = get_app_id(title_requested)
    is_steamapp_found = app_id_details[0]

    if is_steamapp_found:
        steam_app_id = int(app_id_details[1][0])
        title_corrected = app_id_details[1][1]

        owned_games = get_owned_games(player_id_details, steam_api_key)

        if "games" in owned_games["response"]:
            for line in owned_games["response"]["games"]:
                # Read the JSON data file
                if line['appid'] == steam_app_id:
                    game_found = True
                    playtime_forever = line['playtime_forever']
                    playtime_forever = playtime_forever * 60
                    m, s = divmod(playtime_forever, 60)
                    h, m = divmod(m, 60)

                    modules.connection.send_message("%s owns %s and has played for %dhr %02dmin" % (player_name, title_corrected, h, m))
                    break

        if game_found == False:
            modules.connection.send_message("%s doesn't own %s" % (player_name, title_corrected))
            return
    elif not is_steamapp_found and app_id_details[2]:
        modules.connection.send_message("Exact title not found, you can try:")
        for item in app_id_details[2][:results_nb]:  # Display <results_nb> first items
            modules.connection.send_message(item)

    else:
        modules.connection.send_message("Title not found")