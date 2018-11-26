__author__ = 'Djidiouf'

# Python built-in modules
import json  # Library for being able to read Json file
import time  # anti flood if needed: time.sleep(2)
import os       # For instruction related to the OS
import shutil   # Used for OS tools
import configparser
import re  # Regular Expression library
import sys
import requests  # Open url request on website
import operator  # Get item in list
import time  # Give very precise time with time.clock()
import datetime  # Deal with date and allow conversion of date format

# Third-party modules
import html2text  # install html2text

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
    special_chars = ["®", "™", "Tom Clancy's ", "Sid Meier's "]
    title_requested = modules.textalteration.string_cleanup_simple(i_string, special_chars)
    title_requested = title_requested.lower()

    # Condition variables
    title_found = False

    # Results variables
    similar_titles = []
    tup_id = ()

    url_appsid = "http://api.steampowered.com/ISteamApps/GetAppList/v0001/"
    steam_appsid_filename = 'steam_appsid.json'  # Name of the local file
    steam_appsid = retrieve_internet_content(url_appsid, steam_appsid_filename)

    # Read the JSON data file
    for line in steam_appsid['applist']['apps']['app']:
        line['name'] = modules.textalteration.string_cleanup_simple(line['name'], special_chars)  # TODO: Improve perf as this costs a second
        if line['name'].lower() == title_requested:
            title_found = True

            steam_app_id = line['appid']
            steam_app_id = str(steam_app_id)
            title_corrected = line['name']  # Ensure that the correct case is displayed in the future
            tup_id = steam_app_id, title_corrected

            return title_found, tup_id  # End of loop if found

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
    steam_app_id = re.sub("[^0-9]", "", steam_app_id)  # Remove non numeric characters
    return steam_app_id


def get_player_id(i_string, steam_api_key):
    """
    Retrieve the ID of a steam player from Steam API
    Using: http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=XXX&vanityurl=username
    :param i_string:
    :param steam_api_key:
    :return:
    """
    player_id_is_found = False
    player_id = False
    url_steam_player_meta = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=%s&vanityurl=%s' % (steam_api_key, i_string)
    steam_player_id_filename = 'steam_player_id_%s.json' % i_string
    steam_player_id = retrieve_internet_content(url_steam_player_meta, steam_player_id_filename)

    if "steamid" in steam_player_id["response"]:
        player_id = steam_player_id["response"]["steamid"]
        player_id_is_found = True

    return player_id_is_found, player_id


def get_app_metadata(steam_id, cc_code):
    """
    Retrieve the metadata of a title from the Steam API
    :param steam_id:
    :param cc_code:
    :return:
    """
    url_steam_appsmeta = 'http://store.steampowered.com/api/appdetails?appids=%s&cc=%s' % (steam_id, cc_code)
    steam_appsmeta_filename = 'steam_appsmeta_%s_%s.json' % (steam_id, cc_code)
    steam_appsmeta = retrieve_internet_content(url_steam_appsmeta, steam_appsmeta_filename)

    return steam_appsmeta


def get_owned_games(player_id, steam_api_key):
    """
    Retrieve the list of title owned by a player from the Steam API
    :param player_id:
    :param steam_api_key:
    :return:
    """
    url_steam_player_meta = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_played_free_games=1&format=json' % (steam_api_key, player_id)
    steam_player_meta_filename = 'steam_player_meta_%s.json' % player_id
    steam_player_meta = retrieve_internet_content(url_steam_player_meta, steam_player_meta_filename)

    return steam_player_meta


def get_app_review_detailed(steam_id, filter, language, day_range, start_offset, review_type, purchase_type,
                            num_per_page):
    """
    Retrieve the review of a title from the Steam API
    :param steam_id:
    :param filter:            recent, updated, all
    :param language:          see https://partner.steamgames.com/documentation/languages (and use the API language code list) or pass “all” for all reviews
    :param day_range:         range from now to n days ago to look for helpful reviews. Only applicable for the “all” filter.
    :param start_offset:      reviews are returned in batches of 20, so pass 0 for the first set, then 20 for the next set, etc.
    :param review_type:       all, positive, negative
    :param purchase_type:     all, non_steam_purchase, steam
    :param num_per_page:      by default, up to 20 reviews will be returned. More reviews can be returned based on this parameter (with a maximum of 100 reviews)
    :return:
    """
    url_steam_appsreview = 'https://store.steampowered.com/appreviews/%s?json=1&filter=%s&language=%s&day_range=%s&start_offset=%s&review_type=%s&purchase_type=%s&num_per_page=%s' % (
    steam_id, filter, language, day_range, start_offset, review_type, purchase_type, num_per_page)
    steam_appsreview_filename = 'steam_appsreviews_%s.json' % steam_id
    steam_appsreview = retrieve_internet_content(url_steam_appsreview, steam_appsreview_filename)

    return steam_appsreview


def get_app_review_score(steam_id):
    """
    Retrieve the revie of a title from the Steam API for score purposes
    :param steam_id:
    :return:
    """
    url_steam_appsreview_score =\
        'https://store.steampowered.com/appreviews/%s?json=1&filter=%s&language=%s&num_per_page=%s'\
        % (steam_id, 'all', 'all', '1')
    steam_appsreview_score_filename = 'steam_appsreviews_%s_score.json' % steam_id
    steam_appsreview_score = retrieve_internet_content(url_steam_appsreview_score, steam_appsreview_score_filename)

    return steam_appsreview_score


def retrieve_internet_content(i_url, i_filename):
    # Cache properties
    bbot_work_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    cache_steam_dir = bbot_work_dir + 'cache-steam'  # Name of the directory where files will be cached
    cache_age = 1800  # 1800 = 30 min ; 86400 = 24hr
    filename_path = os.path.join(cache_steam_dir, i_filename)  # Name of the local file

    # Other Variables
    now = time.time()
    url = i_url

    # Method CACHE: Retrieve and Store local file --------------
    if not os.path.exists(cache_steam_dir):  # Test if the cache directory exists
        os.makedirs(cache_steam_dir)

    # Download the file if it doesn't exist or is too old
    # TODO: Reverse the if logic
    if not os.path.isfile(filename_path) or os.stat(filename_path).st_mtime < (now - cache_age):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename_path, 'wb') as f:
                f.write(response.content)
            content = response.json()
            return content
    else:
        with open(filename_path, encoding="utf8") as f:
            content = json.load(f)
        return content


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
        if player_id_details[0] is False:
            # modules.connection.send_message("ID not found for player %s" % player_name)
            tup_time = player_name, "(<PlayerID not found>)"
            results.append(tup_time)
            continue

        owned_games = get_owned_games(player_id_details[1], steam_api_key)

        if "games" in owned_games["response"]:
            for line in owned_games["response"]["games"]:
                # Read the JSON data file
                if line['appid'] == steam_app_id:
                    playtime_forever = line['playtime_forever']
                    playtime_forever = playtime_forever * 60
                    m, s = divmod(playtime_forever, 60)
                    h, m = divmod(m, 60)

                    playtime = "(%dh%02dmin)" % (h, m)

                    tup_time = player_name, playtime
                    results.append(tup_time)
                    break

    return results


def steam_admin(i_string, i_medium, i_alias=None):
    cache_steam_dir = 'cache-steam'  # Name of the directory where files will be cached

    if i_string.lower() == "rm-cache":
        shutil.rmtree(cache_steam_dir)
        modules.connection.send_message("Cache has been deleted", i_medium, i_alias)
        return  # Use ** return ** if in a function, exit() otherwise


def steam_inline(i_string, i_medium, i_alias=None):
    # Parse id from URL
    # print(i_string)
    steam_app_id = get_app_id_from_url(i_string)

    # Retrieve all metadata of a specified Steam app for several regions
    country_currency_list = ["fr", "uk", "no"]  # Currency queried in the Steam API
    steam_appsmeta = []
    for country_currency in country_currency_list:
        meta = get_app_metadata(steam_app_id, country_currency)
        steam_appsmeta.append(meta)


    # Test of keys existence
    if "data" in steam_appsmeta[0][steam_app_id]:
        title_corrected = steam_appsmeta[0][steam_app_id]["data"]["name"]

        # Title and Release date
        string_release_date_date = ''
        if "release_date" in steam_appsmeta[0][steam_app_id]["data"]:
            release_date_date = steam_appsmeta[0][steam_app_id]["data"]["release_date"]["date"]

            # Convert release date to a YMD format
            try:
                release_date_date = datetime.datetime.strptime(release_date_date, '%d %b, %Y').strftime('%Y-%m-%d')
            except ValueError:
                pass

            string_release_date_date = " — Released: %s" % release_date_date

        modules.connection.send_message(title_corrected + string_release_date_date, i_medium, i_alias)

        # Retrieve Steam price information
        is_price_found = False
        prices_list=[]
        for item in steam_appsmeta:
            if "price_overview" in item[steam_app_id]["data"]:
                is_price_found = True

                # print(steam_price[steam_app_id]["data"]["price_overview"])  # complete price overview
                price_initial = item[steam_app_id]["data"]["price_overview"]['initial']
                price_discount = item[steam_app_id]["data"]["price_overview"]['discount_percent']
                price_final = item[steam_app_id]["data"]["price_overview"]['final']
                price_currency = item[steam_app_id]["data"]["price_overview"]['currency']

                currency_symbol = ''
                if price_currency == 'AUD':
                    currency_symbol = 'A$'
                elif price_currency == 'EUR':
                    currency_symbol = '€'
                elif price_currency == 'GBP':
                    currency_symbol = '£'
                elif price_currency == 'NOK':
                    currency_symbol = 'kr'

                price_initial = float(price_initial)
                price_initial *= 0.01  # Price was given in cents, switch to a more readable format
                price_discount = int(price_discount)
                price_final = float(price_final)
                price_final *= 0.01  # Price was given in cents, switch to a more readable format

                # Any discount on Steam?
                if price_discount > 0:
                    string_discount = " (-%i%% of %.2f%s)" % (
                        price_discount, price_initial, currency_symbol)
                else:
                    string_discount = ""

                # Create a tuple with price, currency and string discount
                tup_prices = price_final, price_currency, currency_symbol, string_discount
                prices_list.append(tup_prices)

            else:
                continue

        # Create Price string to display
        price_string = "Steam: "
        if is_price_found:
            prices_list.sort(key=operator.itemgetter(1), reverse=False)  # Sort list of prices per 3-letter currency

            for element in prices_list[:-1]:  # Iterate over all but the last item
                price_string += '%.2f%s%s' % (element[0], element[2], element[3])
                price_string += ' | '

            price_string += '%.2f%s%s' % (prices_list[-1][0], prices_list[-1][2], prices_list[-1][3])  # iterate last item
        else:
            price_string += "Not on sale"
        modules.connection.send_message("%s" % price_string, i_medium, i_alias)

        # Give AKS price
        # TODO: fix AKS
        #try:
        #    aks_price_data = modules.steam_secondary.get_russian_price(title_corrected)
        #    if aks_price_data is not None:
        #        modules.connection.send_message("AKS: " + aks_price_data[1] + " — " + aks_price_data[0], i_medium, i_alias)
        #except:
        #    pass


        # Steam additional data: URL, ratings
        # URL
        string_game_url = "http://store.steampowered.com/app/%s" % steam_app_id

        # Metacritic // To be discontinued once reviews are integrated
        string_metacritic = ''
        if "metacritic" in steam_appsmeta[0][steam_app_id]["data"]:
            metacritic_score = steam_appsmeta[0][steam_app_id]["data"]["metacritic"]["score"]
            string_metacritic = " — Metacritic: %s" % metacritic_score

        # Reviews
        string_reviews = ''
        steam_appreview_score = get_app_review_score(steam_app_id)
        if "query_summary" in steam_appreview_score:
            total_positive = int(steam_appreview_score['query_summary']["total_positive"])
            total_reviews = int(steam_appreview_score['query_summary']["total_reviews"])

            if total_reviews > 0:
                score = total_positive * 100 / total_reviews
                string_reviews = " — Reviews: %d%%" % score

        modules.connection.send_message("%s%s%s" % (string_game_url, string_metacritic, string_reviews), i_medium, i_alias)


        # About section
        if "about_the_game" in steam_appsmeta[0][steam_app_id]["data"]:
            price_about_the_game = steam_appsmeta[0][steam_app_id]["data"]["about_the_game"]

            # Substitute with nothing some HTML tags
            price_about_the_game = modules.textalteration.string_replace(price_about_the_game, "\r", " ")
            html_elements = ['<a href=(.*)>', '</a>',
                             '<br>', '<br />',
                             '<h2>', '<h2 class=(.*)>', '</h2>',
                             '<i>', '</i>',
                             '<img src=(.*)>',
                             '<li>', '</li>',
                             '<p>',
                             '<span class=(.*)>', '</span>',
                             '<strong>', '</strong>',
                             '<u>', '</u>',
                             '<ul class=(.*)>', '</ul>']
            price_about_the_game = modules.textalteration.string_cleanup(price_about_the_game, html_elements)

            modules.connection.send_message("About: %s" % price_about_the_game[0:350] + " [...]", i_medium, i_alias)

    else:
        modules.connection.send_message("No info available for this title", i_medium, i_alias)

    # Is the game owned by a predefined list of players?
    owners_records = get_owners(steam_app_id)
    nb_owners = len(owners_records)

    if nb_owners > 0:
        # Cleanup
        modules.connection.send_message("Owned by: %s" % modules.textalteration.list_to_string(owners_records), i_medium, i_alias)
    else:
        modules.connection.send_message("Owned by: nobody", i_medium, i_alias)


def main(i_string, i_medium, i_alias=None):
    """
    Responds to a user that inputs "!steamprice <Game Title>"
    using Steam API: http://api.steampowered.com/ISteamApps/GetAppList/v0001/
    using Steam API: http://store.steampowered.com/api/appdetails?appids=392400&cc=fr

    :param i_string: a string with these elements: "<Game Title>"
    :print: parsed answer about Steam title from the API
    """
    results_nb = 3           # Number of results which will be displayed if an exact natch didn't occur

    tuple_string = i_string.partition(' ')
    sub_cmd = tuple_string[0]
    sub_arg = tuple_string[2]

    if sub_cmd == "admin":
        steam_admin(sub_arg, i_medium, i_alias)
        return
    elif sub_cmd == "played":
        app_id_details = get_app_id(sub_arg.lower())

        is_steamapp_found = app_id_details[0]
        if is_steamapp_found:
            steam_app_id = app_id_details[1][0]

            # Is the game owned by a predefined list of players?
            owners_records = get_owners(steam_app_id)
            nb_owners = len(owners_records)

            if nb_owners > 0:
                modules.connection.send_message("Owned by: %s" % modules.textalteration.list_to_string(owners_records), i_medium, i_alias)
            else:
                modules.connection.send_message("Owned by: nobody", i_medium, i_alias)
        elif not is_steamapp_found and app_id_details[2]:
            if len(app_id_details[2]) > 1:
                modules.connection.send_message("Exact title not found, you can try:", i_medium, i_alias)
                for item in app_id_details[2][:results_nb]:  # Display <results_nb> first items
                    modules.connection.send_message(item, i_medium, i_alias)
            else:
                main("played %s" % app_id_details[2][0], i_medium, i_alias)
        else:
            modules.connection.send_message("Title not found", i_medium, i_alias)
        return
    elif sub_cmd == "own":
        player_owns_game(sub_arg, i_medium, i_alias)
        return
    elif sub_cmd == "spy":
        spy_player(sub_arg, i_medium, i_alias)
        return

    # Main variables
    title_requested = i_string.lower()

    # Retrieve all information, get: (True, ('252490', 'Rust'), ['Rusty Hearts', 'Rusty Hearts Meilin Starter'))
    app_id_details = get_app_id(title_requested)
    is_steamapp_found = app_id_details[0]

    if is_steamapp_found:
        steam_app_id = app_id_details[1][0]
        steam_inline("http://store.steampowered.com/app/%s" % steam_app_id, i_medium, i_alias)

    # Title isn't found
    elif not is_steamapp_found and app_id_details[2]:
        if len(app_id_details[2]) > 1:
            modules.connection.send_message("Exact title not found, you can try:", i_medium, i_alias)
            for item in app_id_details[2][:results_nb]:  # Display <results_nb> first items
                modules.connection.send_message(item, i_medium, i_alias)
        else:
            main(app_id_details[2][0], i_medium, i_alias)

    else:
        modules.connection.send_message("Title not found", i_medium, i_alias)


def spy_player(i_string, i_medium, i_alias=None):
    """
    Responds to a user that inputs "!steam spy <PlayerName>"
    :param i_string:
    :return:
    """
    player_name = i_string
    has_played = False

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    steam_api_key = config['API_keys']['steam']

    # Retrieve player ID
    player_id_details = get_player_id(player_name, steam_api_key)
    if player_id_details[0] is False:
        modules.connection.send_message("ID not found for player %s" % player_name, i_medium, i_alias)
        return

    owned_games = get_owned_games(player_id_details[1], steam_api_key)

    modules.connection.send_message("In the last 2 weeks %s has played:" % player_name, i_medium, i_alias)
    playtime_2_weeks_total = 0

    # List of games titles and playtimes
    games_played=[]

    if "games" in owned_games["response"]:
        for line in owned_games["response"]["games"]:
            if "playtime_2weeks" in line:
                has_played = True
                steam_app_id = line['appid']
                steam_appsmeta = get_app_metadata(steam_app_id, "fr")
                try:
                    title_corrected = steam_appsmeta['%s' % steam_app_id]["data"]["name"]
                except KeyError:
                    title_corrected = "<Game deleted from the Steam Store>"
                playtime_2weeks = line['playtime_2weeks']
                playtime_2weeks = playtime_2weeks * 60

                # Create a tuple with both the game's title and playtime
                tup_time = title_corrected, playtime_2weeks
                games_played.append(tup_time)

                playtime_2_weeks_total = playtime_2_weeks_total + playtime_2weeks

    # Display a sorted list of game titles and playtime
    games_played.sort(key=operator.itemgetter(1), reverse=True)

    for element in games_played:
        title_corrected = element[0]
        m, s = divmod(element[1], 60)
        h, m = divmod(m, 60)
        modules.connection.send_message("- %s (%dh%02dmin)" % (title_corrected, h, m), i_medium, i_alias)
        time.sleep(0.1)  # Reduce output speed for flood prevention

    # Display total playtime
    if has_played:
        # Total
        m_t, s_t = divmod(playtime_2_weeks_total, 60)
        h_t, m_t = divmod(m_t, 60)

        # Average
        playtime_2_weeks_total = playtime_2_weeks_total / 14
        m_a, s_a = divmod(playtime_2_weeks_total, 60)
        h_a, m_a = divmod(m_a, 60)

        modules.connection.send_message(
            "For a total of %dh%02dmin (average of %dh%02dmin per day)" % (h_t, m_t, h_a, m_a), i_medium, i_alias)
    else:
        modules.connection.send_message("Nothing at all.", i_medium, i_alias)


def player_owns_game(i_string, i_medium, i_alias=None):
    """
    Responds to a user that inputs "!steam own <PlayerName> <GameTitle>"
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
    if player_id_details[0] is False:
        modules.connection.send_message("ID not found for player %s" % player_name, i_medium, i_alias)
        return

    # Retrieve steam app ID
    app_id_details = get_app_id(title_requested)
    is_steamapp_found = app_id_details[0]

    if is_steamapp_found:
        steam_app_id = int(app_id_details[1][0])
        title_corrected = app_id_details[1][1]

        owned_games = get_owned_games(player_id_details[1], steam_api_key)

        if "games" in owned_games["response"]:
            for line in owned_games["response"]["games"]:
                # Read the JSON data file
                if line['appid'] == steam_app_id:
                    game_found = True
                    playtime_forever = line['playtime_forever']
                    playtime_forever = playtime_forever * 60
                    m, s = divmod(playtime_forever, 60)
                    h, m = divmod(m, 60)

                    modules.connection.send_message("%s has played %s for %dh%02dmin" % (player_name, title_corrected, h, m), i_medium, i_alias)
                    break

        if game_found is False:
            modules.connection.send_message("%s doesn't own %s" % (player_name, title_corrected), i_medium, i_alias)
            return
    elif not is_steamapp_found and app_id_details[2]:
        modules.connection.send_message("Exact title not found, you can try:", i_medium, i_alias)
        for item in app_id_details[2][:results_nb]:  # Display <results_nb> first items
            modules.connection.send_message(item, i_medium, i_alias)

    else:
        modules.connection.send_message("Title not found", i_medium, i_alias)
