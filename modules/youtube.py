__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website
import json  # Library for being able to read Json file
import os       # For instruction related to the OS
import configparser

# Project modules
import modules.connection


def get_ytchannel_metadata(i_string, ytdata_api_key):

    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id=%s&key=%s' % (i_string, ytdata_api_key)

    ytchannel_metadata = urllib.request.urlopen(url)
    ytchannel_metadata = ytchannel_metadata.read().decode('utf-8')
    ytchannel_json = json.loads(ytchannel_metadata)

    if "items" in ytchannel_json:
        if "statistics" in ytchannel_json["items"][0]:
            view_count = ytchannel_json["items"][0]["statistics"]['viewCount']
            video_count = ytchannel_json["items"][0]["statistics"]['videoCount']
            sub_count = ytchannel_json["items"][0]["statistics"]['subscriberCount']

            modules.connection.send_message("Videos: %s - Views: %s - Subs: %s" % (video_count, view_count, sub_count))

            modules.connection.send_message("Channel: https://www.youtube.com/channel/%s" % i_string)


def main(i_string):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    youtube_data_api_key = config['API_keys']['youtube_data']

    get_ytchannel_metadata(i_string, youtube_data_api_key)
