__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website
import json  # Library for being able to read Json file
import time  # anti flood if needed: time.sleep(2)
import os       # For instruction related to the OS
import shutil   # Used for OS tools
import configparser
import re  # Regular Expression library

# Project modules
import modules.textalteration
import modules.connection
import modules.steam_secondary


def get_app_id(i_string):
    """
    Get the ID of a steam title from Steam API
    :param i_string:
    :return: if the title has been found, the ID, the correct title, a list of approximative titles
    INPUT   OUTPUT
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
        # DEBUG modules.connection.send_message("Cache outdated (> %dhr %02dmin), retrieving new Steam apps list ..." % (h, m))
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

    # Sort similar_titles list alphabetically
    similar_titles = sorted(similar_titles, key=str.lower)

    result = title_found, tup_id, similar_titles
    return result


def get_app_id_from_url(i_string):
    # divide a string in a tuple: 'str1', 'separator', 'str2'
    parse_url = modules.textalteration.string_split(i_string, "/", "?")
    steam_app_id = str(parse_url[4])  # Give app id
    steam_app_id = re.sub("[^0-9]", "", steam_app_id) # Remove non numeric characters
    return steam_app_id


def get_player_id(i_string, steam_api_key):
    """
    Retrieve the ID of a steam player from Steam API
    Using: http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=XXX&vanityurl=username
    :param i_string:
    :param steam_api_key:
    :return:
    """
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
        # DEBUG modules.connection.send_message("Retrieving ID for player %s ..." % i_string)
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
    """
    Retrieve the metadata of a title from the Steam API
    :param steam_id:
    :param cc_code:
    :return:
    """
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
        # DEBUG modules.connection.send_message("Title found (%s), retrieving last metadata ..." % steam_id)
        urllib.request.urlretrieve(url_steam_appsmeta, filename=steam_appsmeta_filename)

    with open(steam_appsmeta_filename, encoding="utf8") as f:
        steam_appsmeta = json.load(f)

    return steam_appsmeta


def get_owned_games(player_id, steam_api_key):
    """
    Retrieve the list of title owned by a player from the Steam API
    :param player_id:
    :param steam_api_key:
    :return:
    """
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    # Time variables
    now = time.time()
    cache_age = 86400  # 86400 = 24hr

    url_steam_player_meta = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_played_free_games=1&format=json' % (steam_api_key, player_id)

    # Method CACHE: Retrieve and Store local file --------------
    if not os.path.exists(cache_steam_dir):  # Test if the directory exists
        os.makedirs(cache_steam_dir)
    steam_player_meta_filename = 'steam_player_meta_%s.json' % player_id
    steam_player_meta_filename = os.path.join(cache_steam_dir, steam_player_meta_filename)  # Name of the local file

    # Download the file if it doesn't exist or is too old
    if not os.path.isfile(steam_player_meta_filename) or os.stat(steam_player_meta_filename).st_mtime < (now - cache_age):
        # DEBUG modules.connection.send_message("Player found (%s), retrieving last metadata ..." % player_id)
        urllib.request.urlretrieve(url_steam_player_meta, filename=steam_player_meta_filename)

    with open(steam_player_meta_filename, encoding="utf8") as f:
        steam_player_meta = json.load(f)

    return steam_player_meta


def get_owners(steam_id):
    # Determine if a game is own by a list of predefined people
    steam_app_id = int(steam_id)  # Need to be an int

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    steam_api_key = config['API_keys']['steam']

    # Retrieve player name from config file
    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    player_names = config['steam']['owners'].split(',')

    # Results variables
    results = []

    for player_name in player_names:

        # Retrieve player ID
        player_id_details = get_player_id(player_name, steam_api_key)
        if player_id_details is None:
            return

        owned_games = get_owned_games(player_id_details, steam_api_key)

        if "games" in owned_games["response"]:
            for line in owned_games["response"]["games"]:
                # Read the JSON data file
                if line['appid'] == steam_app_id:
                    playtime_forever = line['playtime_forever']
                    playtime_forever = playtime_forever * 60
                    m, s = divmod(playtime_forever, 60)
                    h, m = divmod(m, 60)

                    playtime = "(%dh%02dmin)" % (h,m)

                    tup_time = player_name, playtime
                    results.append(tup_time)
                    break

    return results


def steam(i_string):
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    if i_string.lower() == "@rm-cache":
        shutil.rmtree(cache_steam_dir)
        modules.connection.send_message("Cache has been deleted")
        return  # Use ** return ** if in a function, exit() otherwise


def steam_inline(i_string):
    # Parse id from URL
    steam_app_id = get_app_id_from_url(i_string)

    country_currency = "fr"  # Currency queried in the Steam API

    # Price and info
    # Retrieve all metadata of a specified Steam app
    steam_appsmeta = get_app_metadata(steam_app_id, country_currency)

    # Test of keys existence
    if "data" in steam_appsmeta[steam_app_id]:
        title_corrected = steam_appsmeta[steam_app_id]["data"]["name"]

        if "metacritic" in steam_appsmeta[steam_app_id]["data"]:
            price_metacritic_score = steam_appsmeta[steam_app_id]["data"]["metacritic"]["score"]
            string_metacritic=" — Metacritic: %s" % price_metacritic_score
        else:
            string_metacritic=""

        modules.connection.send_message(title_corrected + string_metacritic)

        # Give Steam price
        if "price_overview" in steam_appsmeta[steam_app_id]["data"]:
            # print(steam_price[steam_app_id]["data"]["price_overview"])  # complete price overview
            price_initial = steam_appsmeta[steam_app_id]["data"]["price_overview"]['initial']
            price_discount = steam_appsmeta[steam_app_id]["data"]["price_overview"]['discount_percent']
            price_final = steam_appsmeta[steam_app_id]["data"]["price_overview"]['final']
            price_currency = steam_appsmeta[steam_app_id]["data"]["price_overview"]['currency']
            if price_currency == 'EUR':
                price_currency = '€'

            price_initial = float(price_initial)
            price_initial *= 0.01  # Price was given in cents, switch to a more readable format
            price_discount = int(price_discount)
            price_final = float(price_final)
            price_final *= 0.01  # Price was given in cents, switch to a more readable format

            # Any discount on Steam?
            if price_discount > 0:
                string_discount = " (-%i%% of %.2f%s)" % (
                                            price_discount,price_initial, price_currency)
            else:
                string_discount = ""

            modules.connection.send_message("Steam: %.2f%s" % (price_final, price_currency) + string_discount
                                            + " — http://store.steampowered.com/app/%s" % steam_app_id)
        else:
            modules.connection.send_message("Steam: Not on sale" + " — http://store.steampowered.com/app/%s" % steam_app_id)

        # Give AKS price
        try:
            aks_price_data = modules.steam_secondary.get_russian_price(title_corrected)
            if aks_price_data != None:
                modules.connection.send_message("AKS: " + aks_price_data[1] + " — " + aks_price_data[0])
        except:
            pass

        if "about_the_game" in steam_appsmeta[steam_app_id]["data"]:
            price_about_the_game = steam_appsmeta[steam_app_id]["data"]["about_the_game"]

            # Substitute with nothing some html
            price_about_the_game = modules.textalteration.string_replace(price_about_the_game, "\r", " ")
            html_elements = ["<p>", "<br>", "<br />", "<strong>", "</strong>", "<i>", "</i>", '<img src="(.*)">',
                             "<h2>", "</h2>", "<li>", "</li>", '<ul class="(.*)">', "</ul>", '<a href="(.*)">', "</a>"]
            price_about_the_game = modules.textalteration.string_cleanup(price_about_the_game, html_elements)

            modules.connection.send_message("About: %s" % price_about_the_game[0:350] + " [...]")

    else:
        modules.connection.send_message("No info available for this title")

    # Is the game owned by a predefined list of players?
    owners_records = get_owners(steam_app_id)
    nb_owners = len(owners_records)

    if nb_owners > 0:
        # Cleanup
        owners_records = str(owners_records)[1:-1]
        owners_records = modules.textalteration.string_replace(owners_records, "', '", " ")
        owners_records = modules.textalteration.string_replace(owners_records, "'), ('", ", ")
        owners_records = modules.textalteration.string_replace(owners_records, "('", "")
        owners_records = modules.textalteration.string_replace(owners_records, "')", "")
        modules.connection.send_message("Owned by: %s" % owners_records)
    else:
        modules.connection.send_message("Owned by: nobody")


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

    results_nb = 3           # Number of results which will be displayed if an exact natch didn't occur

    # Retrieve all information, get: (True, ('252490', 'Rust'), ['Rusty Hearts', 'Rusty Hearts Meilin Starter'))
    app_id_details = get_app_id(title_requested)
    is_steamapp_found = app_id_details[0]

    if is_steamapp_found:
        steam_app_id = app_id_details[1][0]
        steam_inline("http://store.steampowered.com/app/%s" % steam_app_id)

    # Title isn't found
    elif not is_steamapp_found and app_id_details[2]:
        modules.connection.send_message("Exact title not found, you can try:")
        for item in app_id_details[2][:results_nb]:  # Display <results_nb> first items
            modules.connection.send_message(item)

    else:
        modules.connection.send_message("Title not found")


def player_owns_game(i_string):
    """
    Responds to a user that inputs "!steamown <PlayerName> <GameTitle>"
    :param i_string:
    :return:
    """
    tuple_string = i_string.partition(' ')
    player_name = tuple_string[0]
    title_requested = tuple_string[2]

    if title_requested == "":
        raise ValueError('An argument is missing')

    game_found = False
    results_nb = 3  # Number of results which will be displayed if an exact natch didn't occur

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

                    modules.connection.send_message("%s has played %s for %dh %02dmin" % (player_name, title_corrected, h, m))
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
