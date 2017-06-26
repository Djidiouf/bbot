__author__ = 'Djidiouf'

# Python built-in modules
import re
import configparser
import os

# Third-party modules
import langdetect  # install langdetect
import requests  # install requests
import html2text  # install html2text
import goslate  # install goslate | translate text

# Project modules
import modules.textalteration
import modules.connection


# Retrieve player name from config file
config = configparser.ConfigParser()
config.read(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
notfrom_languages = config['translate']['lang_ignored'].split(',')
translated_languages = config['translate']['lang_output'].split(',')


# remove unwanted chars at the end of urls
def clean_url(i_string):
    cleaned_string = i_string
    char_to_remove = (')', '.', ',', '?', '!', '"', "'", ':', '\\', '/')

    for each in char_to_remove:
        cleaned_string = cleaned_string.rstrip(each)
    return cleaned_string

def translate_inline(i_string):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i_string)

    for url in urls:
        url = clean_url(url)

        webpage_src = requests.get(url)  # Retrieve URL data

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

            # modules.connection.send_message( url + " — Language probability: " + str(languages_detected)[1:-1])

            source_language = str(languages_detected[0]).split(":")

            if source_language[0] not in notfrom_languages:
                for language in translated_languages:
                    modules.connection.send_message("Translated in %s: " % (language) +
                                                    "https://translate.google.com/translate?sl=%s&tl=%s&js=y&prev=_t&hl=en&ie=UTF-8&u=%s"
                                                    % (source_language[0], translated_languages[0], url))
        else:
            # Disregard such url
            pass
