__author__ = 'Djidiouf'

# Python built-in modules
import re
import configparser
import os

# Third-party modules
import langdetect  # install langdetect
import requests  # install requests
import html2text  # install html2text

# Project modules
import modules.textalteration
import modules.connection


# remove unwanted chars at the end of urls
def clean_url(i_string):
    cleaned_string = i_string
    char_to_remove = (')', '.', ',', '?', '!', '"', "'", ':', '\\', '/')

    for each in char_to_remove:
        cleaned_string = cleaned_string.rstrip(each)
    return cleaned_string

def main(i_string, i_medium, i_alias=None):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i_string)

    # Retrieve player name from config file
    config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    lang_ignored = config['translate']['lang_ignored'].split(',')
    lang_output = config['translate']['lang_output'].split(',')

    for url in urls:
        url = clean_url(url)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        webpage_src = requests.get(url, headers=headers)  # Retrieve URL data

        # Check if data contain text or not
        if "text/html" in webpage_src.headers["content-type"]:
            webpage_src = webpage_src.text
            # webpage_title = webpage_src[webpage_src.find('<title>') + 7: webpage_src.find('</title>')]

            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            h.images_to_alt = True
            webpage = h.handle(webpage_src)  # Retrieve only the text without any html tags

            languages_detected = langdetect.detect_langs(webpage)

            # Debug
            # modules.connection.send_message(webpage.split('\n', 1)[0])
            # modules.connection.send_message( url + " — Language probability: " + str(languages_detected)[1:-1])

            source_language = str(languages_detected[0]).split(":")

            if source_language[0] not in lang_ignored:
                for language in lang_output:
                    modules.connection.send_message("Translated in %s: " % (language) +
                                                    "https://translate.google.com/translate?sl=%s&tl=%s&js=y&prev=_t&hl=en&ie=UTF-8&u=%s"
                                                    % (source_language[0], language, url), i_medium, i_alias)
        else:
            # Disregard such url
            pass
