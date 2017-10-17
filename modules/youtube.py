__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website
import urllib.error
import urllib.parse
import json  # Library for being able to read Json file
import os       # For instruction related to the OS
import configparser

# Project modules
import modules.textalteration
import modules.connection


class MyExceptionYtNoExistence(Exception):
    """Raise for my specific kind of exception"""
    pass


def get_ytchannel_metadata(i_string, ytdata_api_key):

    # Load json output
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id=%s&key=%s' % (i_string, ytdata_api_key)
    ytchannel_metadata = urllib.request.urlopen(url)
    ytchannel_metadata = ytchannel_metadata.read().decode('utf-8')
    ytchannel_json = json.loads(ytchannel_metadata)

    # NEED TO CHECK: not triggered as a 400 error is raised by Google server even if they have served a json
    if "error" in ytchannel_json:
        if "errors" in ytchannel_json["error"]:
            if "reason" in ytchannel_json["error"]["errors"][0]:
                reason = ytchannel_json["error"]["errors"][0]['reason']
                modules.connection.send_message("The attempt to retrieve that channel failed. Reason: %s" % reason)
                raise MyExceptionYtNoExistence("Unbelievable YT server error: %s" % reason)
        return  # Use ** return ** if in a function, exit() otherwise

    if "items" in ytchannel_json:
        if len(ytchannel_json["items"]) > 0:
            if "statistics" in ytchannel_json["items"][0]:
                view_count = ytchannel_json["items"][0]["statistics"]['viewCount']
                video_count = ytchannel_json["items"][0]["statistics"]['videoCount']
                sub_count = ytchannel_json["items"][0]["statistics"]['subscriberCount']

                return video_count, view_count, sub_count, "https://www.youtube.com/channel/%s" % i_string
        else:
            raise MyExceptionYtNoExistence("This channel doesn't exist")


def get_id(i_string, yt_data_api_key):

    i_string = modules.textalteration.string_replace(i_string, ' ', '+')  # Spaces need to be replace in the url

    # Parse the arguments needed for channel with accents
    ytchannel_id_url_half_detailed = "q=%s&type=channel&key=%s" % (urllib.parse.quote(i_string), yt_data_api_key)
    ytchannel_id = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/search?part=snippet&" + ytchannel_id_url_half_detailed)

    ytchannel_id = ytchannel_id.read().decode('utf-8')
    ytchannel_id_json = json.loads(ytchannel_id)

    if "items" in ytchannel_id_json:
        if len(ytchannel_id_json["items"]) > 0:
            if "id" in ytchannel_id_json["items"][0]:
                channel_id = ytchannel_id_json["items"][0]["id"]['channelId']
                return channel_id
    else:
        raise MyExceptionYtNoExistence("This channel doesn't exist")


def main(i_string, i_medium, i_alias=None):
    # Retrieve API key
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
    youtube_data_api_key = config['API_keys']['youtube_data']

    try:
        display_name = get_id(i_string, youtube_data_api_key)
    except urllib.error.HTTPError:
        modules.connection.send_message("Bad request, (perhaps the YT API key)", i_medium, i_alias)
        return
    except MyExceptionYtNoExistence as e:
        modules.connection.send_message(e.args, i_medium, i_alias)
        return

    try:
        yt_metadata = get_ytchannel_metadata(display_name, youtube_data_api_key)
        modules.connection.send_message("Videos: %s - Views: %s - Subs: %s" %
                                        (yt_metadata[0], yt_metadata[1], yt_metadata[2]), i_medium, i_alias)
        modules.connection.send_message("Channel: %s" % yt_metadata[3], i_medium, i_alias)
    except urllib.error.HTTPError:
        modules.connection.send_message("Bad request, (perhaps the YT API key)", i_medium, i_alias)
        return
    except MyExceptionYtNoExistence as e:
        modules.connection.send_message("%s" % e.args, i_medium, i_alias)
        return
