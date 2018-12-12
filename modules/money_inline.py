__author__ = 'Djidiouf'

# Python built-in modules
import configparser
import re
import requests
import os

# Project modules
import modules.connection
import modules.meta_download
import modules.textalteration

# Read config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better
blacklisted_currencies = config['money_inline']['blacklisted_currencies'].split(",")


def get_rate(code1, code2):
    url = 'https://free.currencyconverterapi.com/api/v6/convert?q=%s_%s&compact=y' % (code1, code2)

    filename = 'rate_%s_%s.json' % (code1, code2)
    return modules.meta_download.dl_url_content(url, filename, 'cache-money', 86400)


def main(i_string, i_medium, i_alias=None):

    # Capitalize the full string to not have to bother between eur and EUR or a$ and A$
    i_string = i_string.upper()

    all_cur = re.findall(r"(?:A\$|\$|\€|\£)[0-9|\,|\.|\s|\']+|(?:\d\s|\d|\.\d)[0-9|\,|\.|\s|\']*[a-zA-Z]{3}\b|\d[0-9|\,|\.|\'|\s]*(?:A\$|\$|\s\$|\€|\£)",
                         i_string)  # https://regex101.com/r/eI8wlW/7
    # by group: ((?:A\$|\$|\€|\₤)[0-9|\,|\.|\s|\']+)|((?:\d\s|\d|\.\d)[0-9|\,|\.|\s|\']*[a-zA-Z]{3}\b)|(\d[0-9|\,|\.|\'|\s]*+(?:A\$|\$|\s\$|\€|\₤))

    for item in all_cur:
        # Cleanup matches from unwanted separators
        not_wanted = [" ", "'"]
        item = modules.textalteration.string_cleanup_simple(item, not_wanted)

        # English format of 1,000,000.00
        if "," in item and "." in item:
            item = modules.textalteration.string_cleanup_simple(item, ",")

        # Fix floating notation when coma are in used
        if "," in item:
            item = modules.textalteration.string_replace(item, ",", ".")

        # Fix multiple floating dot and keep only the first one in string
        item = re.sub('\.(?=.*?\.)', '', item)

        # By default, currency is considered defined as a ISO suffix
        item_type = 'suffix'

        # Replace prefixed symbols by ISO suffixes
        if item[0] == 'A' and item[1] == '$':
            item = modules.textalteration.string_cleanup_simple(item, "A$")
            item = item + ' ' + 'AUD'
            item_type = 'prefix'
        elif item[0] == '$':
            item = modules.textalteration.string_cleanup_simple(item, "$")
            item = item + ' ' + 'USD'
            item_type = 'prefix'
        elif item[0] == '€':
            item = modules.textalteration.string_cleanup_simple(item, "€")
            item = item + ' ' + 'EUR'
            item_type = 'prefix'
        elif item[0] == '£':
            item = modules.textalteration.string_cleanup_simple(item, "£")
            item = item + ' ' + 'GBP'
            item_type = 'prefix'

        # Replace suffixed symbols by ISO suffixes
        if item[-2] == 'A' and item[-1] == '$':
            item = modules.textalteration.string_cleanup_simple(item, "A$")
            item = item + '' + 'AUD'
        elif item[-1] == '$':
            item = modules.textalteration.string_cleanup_simple(item, "$")
            item = item + '' + 'USD'
        elif item[-1] == '€':
            item = modules.textalteration.string_cleanup_simple(item, "€")
            item = item + '' + 'EUR'
        elif item[-1] == '£':
            item = modules.textalteration.string_cleanup_simple(item, "£")
            item = item + '' + 'GBP'

        # Prefix floating character by 0 if needed to avoid .35 AUD
        if item.startswith('.'):
            item = item[:0] + "0" + item[0:]

        # Separate amount from currency code with a space
        if item_type == "suffix":
            item = re.sub(r'([A-Z]{3})', r" \1", item)

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_string = item.partition(' ')
        amount = tuple_string[0]
        code = tuple_string[2]

        # Blacklist currency codes
        if code in blacklisted_currencies:
            return

        # amount needs to be int and not string
        amount = float(amount)

        try:
            rate_aud = get_rate(code, "AUD")
            key_aud = "%s_%s" % (code, 'AUD')
            rate_eur = get_rate(code, "EUR")
            key_eur = "%s_%s" % (code, 'EUR')
            rate_gbp = get_rate(code, "GBP")
            key_gbp = "%s_%s" % (code, 'GBP')
            rate_nok = get_rate(code, "NOK")
            key_nok = "%s_%s" % (code, 'NOK')

            total_aud = '{:,.2f}'.format(amount * rate_aud[key_aud]['val']).replace(',', ' ')
            total_eur = '{:,.2f}'.format(amount * rate_eur[key_eur]['val']).replace(',', ' ')
            total_gbp = '{:,.2f}'.format(amount * rate_gbp[key_gbp]['val']).replace(',', ' ')
            total_nok = '{:,.2f}'.format(amount * rate_nok[key_nok]['val']).replace(',', ' ')
        except:
            continue

        amount = '{:,.2f}'.format(amount).replace(',', ' ')

        if code not in ["AUD", "EUR", "GBP", "NOK"]:
            # 305 546.00 USD = 512 589.24 AUD | 314 844.94 EUR | 215 584.12 GBP | 3 000 000.00 NOK
            message = "%s %s" % (amount, code) + " = " + "%s %s" % (total_aud, "AUD") + " | " + "%s %s" % (total_eur, "EUR") + " | " + "%s %s" % (total_gbp, "GBP") + " | " + "%s %s" % (total_nok, "NOK")
        elif code == "AUD":
            message = "%s %s" % (amount, code) + " = " + "%s %s" % (total_eur, "EUR") + " | " + "%s %s" % (total_gbp, "GBP") + " | " + "%s %s" % (total_nok, "NOK")
        elif code == "EUR":
            message = "%s %s" % (amount, code) + " = " + "%s %s" % (total_aud, "AUD") + " | " + "%s %s" % (total_gbp, "GBP") + " | " + "%s %s" % (total_nok, "NOK")
        elif code == "GBP":
            message = "%s %s" % (amount, code) + " = " + "%s %s" % (total_aud, "AUD") + " | " + "%s %s" % (total_eur, "EUR") + " | " + "%s %s" % (total_nok, "NOK")
        elif code == "NOK":
            message = "%s %s" % (amount, code) + " = " + "%s %s" % (total_aud, "AUD") + " | " + "%s %s" % (total_eur, "EUR") + " | " + "%s %s" % (total_gbp, "GBP")


        modules.connection.send_message(message, i_medium, i_alias)
