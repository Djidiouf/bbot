__author__ = 'Djidiouf'

# Python built-in modules
import json  # Library for being able to read Json file
import os       # For instruction related to the OS
import sys
import requests  # Open url request on website
import urllib.request  # Open url request on website
import urllib.error  # Manage errors for urllib
import time  # Give very precise time with time.clock()

# Third-party modules
##

# Project modules
##


def dl_url_content(i_url, i_filename, i_folder, i_cache_age=None):
    # Cache properties
    bbot_work_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
    cache_dir = bbot_work_dir + i_folder  # Name of the directory where files will be cached
    filename_path = os.path.join(cache_dir, i_filename)  # Name of the local file

    if i_cache_age is None:
        i_cache_age = 0  # 1800 = 30 min ; 86400 = 24hr

    # Other Variables
    now = time.time()
    url = i_url
    retrieve_method = "urllib"

    # Method CACHE: Retrieve and Store local file --------------
    if not os.path.exists(cache_dir):  # Test if the cache directory exists
        os.makedirs(cache_dir)

    # Download the file if it doesn't exist or is too old
    # TODO: Reverse the if logic for testing file presence + age
    if retrieve_method == "requests":
        if not os.path.isfile(filename_path) or os.stat(filename_path).st_mtime < (now - i_cache_age):
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
    elif retrieve_method == "urllib":
        if not os.path.isfile(filename_path) or os.stat(filename_path).st_mtime < (now - i_cache_age):
            try:
                response = urllib.request.urlopen(url).read()
            except urllib.error.URLError as e:
                pass

            with open(filename_path, 'wb') as f:
                f.write(response)
            content = json.loads(response.decode('utf-8'))

            return content
        else:
            with open(filename_path, encoding="utf8") as f:
                content = json.load(f)
            return content
