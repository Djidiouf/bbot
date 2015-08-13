__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website
import urllib.parse
import json  # Library for being able to read Json file

# Project modules
import modules.connection
import modules.textalteration


def imdb_info(i_string):
    """
    Responds to a user that inputs:
                                    "!imdb <Guessed Title>"
                                    "!imdb <Guessed Title>#<Year>"
                                    "!imdb i:<imdbID>"

    using The Open Movie Database API: http://www.omdbapi.com

    :param i_string: a string with these elements: "<Guessed Title>" or <Guessed Title>#<Year>" or "<imdbID>"
    :print: parsed answer about a imdb title from the API
    """
    movie_found = False

    i_string = i_string.lower()

    tuple_string = i_string.partition('#')
    part_one = tuple_string[0]
    part_two = tuple_string[2]


    if not part_one.startswith("id:"):
        part_one = modules.textalteration.string_replace(part_one, ' ', '+')  # Spaces need to be replace in the url

        # Parse of the arguments needed for movies with accents
        omdb_url_half_detailed = "t=%s&y=%s&plot=short&r=json" % ((urllib.parse.quote(part_one),part_two))
        omdb_request_api = urllib.request.urlopen("http://www.omdbapi.com/?" + omdb_url_half_detailed)

        omdb_request_api = omdb_request_api.read().decode('utf-8')

        omdb_json = json.loads(omdb_request_api)


        if "Response" in omdb_json and omdb_json["Response"] == "True":
            movie_found = True

    if part_one.startswith("id:"):
        # Separation of id:tt0411008
        tuple_id = part_one.partition(':')
        imdb_id = tuple_id[2]

        omdb_url_full_detailed = 'http://www.omdbapi.com/?i=%s&plot=short&r=json' % imdb_id
        omdb_request_api = urllib.request.urlopen(omdb_url_full_detailed).read().decode('utf-8')
        omdb_json = json.loads(omdb_request_api)

        if "Response" in omdb_json and omdb_json["Response"] == "True":
            movie_found = True

        # A json file is there whatever is requested.
        # "Response" is True if the imdb title exists
        # "Response" is False if not
    if movie_found:
        if "Title" in omdb_json and "Released" in omdb_json:
            movie_title = omdb_json["Title"]
            movie_released = omdb_json["Released"]
            modules.connection.send_message("Title: %s (Release date: %s)" % (movie_title, movie_released))

        if "Country" in omdb_json and "Runtime" in omdb_json and "Genre" in omdb_json:
            movie_country = omdb_json["Country"]
            movie_runtime = omdb_json["Runtime"]
            movie_genre = omdb_json["Genre"]
            modules.connection.send_message("%s - %s - %s" % (movie_country, movie_runtime, movie_genre))

        if "Plot" in omdb_json:
            movie_plot = omdb_json["Plot"]
            modules.connection.send_message("Plot: %s" % movie_plot)

        if "imdbID" in omdb_json and "imdbRating" in omdb_json:
            movie_imdbid = omdb_json["imdbID"]
            movie_imdbrating = omdb_json["imdbRating"]
            modules.connection.send_message("imdbID: %s - Rating: %s" % (movie_imdbid, movie_imdbrating))
    else:
        modules.connection.send_message("IMDB title not found!")
