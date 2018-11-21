__author__ = 'Djidiouf'

# Python built-in modules
import re
import requests

# Project modules
import modules.connection
import modules.textalteration


def get_rate(code1, code2):
    url = 'https://free.currencyconverterapi.com/api/v5/convert?q=%s_%s&compact=y' % (code1, code2)
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        content = response.json()

        key = "%s_%s" % (code1, code2)
        rate = content[key]["val"]
        rate = float(rate)
        return rate

def main(i_string, i_medium, i_alias=None):

    # Capitalize the full string to not have to bother between eur and EUR or a$ and A$
    i_string = i_string.upper()

    all_cur = re.findall(r"(?:a\$|\$|\€|\₤)[0-9|\,|\.|\s|\']+|(?:\d\s|\d|\.\d)[0-9|\,|\.|\s|\']*[a-zA-Z]{3}\b|\d[0-9|\,|\.|\'|\s]*+(?:a\$|\$|\s\$|\€|\₤)",
                         i_string)  # https://regex101.com/r/eI8wlW/6
    # by group: ((?:a\$|\$|\€|\₤)[0-9|\,|\.|\s|\']+)|((?:\d\s|\d|\.\d)[0-9|\,|\.|\s|\']*[a-zA-Z]{3}\b)|(\d[0-9|\,|\.|\'|\s]*+(?:a\$|\$|\s\$|\€|\₤))


    for item in all_cur:
        # Cleanup matches from unwanted separators
        not_wanted = [" ", "'"]
        item = modules.textalteration.string_cleanup(item, not_wanted)

        # English format of 1,000,000.00
        if "," in item and "." in item:
            item = modules.textalteration.string_cleanup(item, ",")

        # Fix floating notation when coma are in used
        if "," in item:
            item = modules.textalteration.string_replace(item, ",", ".")

        # By default, currency is considered defined as a suffix
        item_type = 'suffix'

        # Replace prefixes by suffixes
        if item[0] == '$':
            item = modules.textalteration.string_cleanup(item, "$")
            item = item + ' ' + 'USD'
            item_type = 'prefix'
        elif item[0] == '€':
            item = modules.textalteration.string_cleanup(item, "€")
            item = item + ' ' + 'EUR'
            item_type = 'prefix'
        elif item[0] == '₤':
            item = modules.textalteration.string_cleanup(item, "₤")
            item = item + ' ' + 'GBP'
            item_type = 'prefix'
        elif item[0] == 'A' and item[1] == '$':
            item = modules.textalteration.string_cleanup(item, "A$")
            item = item + ' ' + 'AUD'
            item_type = 'prefix'

        # Prefix floating character by 0 if needed to avoid .35 AUD
        if item.startswith('.'):
            item = item[:0] + "0" + item[0:]

        # Separate amount from currency code
        if item_type == "suffix":
            item = re.sub(r'([A-Z]{3})',r" \1",item)

        # Debug print
        # print(item_type + ": " + item)

        # divide a string in a tuple: 'str1', 'separator', 'str2'
        tuple_string = item.partition(' ')
        amount = tuple_string[0]
        code = tuple_string[2]

        # amount needs to be int and not string
        amount = float(amount)

        try:
            rate_aud = get_rate(code, "AUD")
            rate_eur = get_rate(code, "EUR")
            rate_gbp = get_rate(code, "GBP")
            rate_nok = get_rate(code, "NOK")
        except:
            continue

        total_aud = amount * rate_aud
        total_eur = amount * rate_eur
        total_gbp = amount * rate_gbp
        total_nok = amount * rate_nok

        if code not in ["AUD", "EUR", "GBP", "NOK"]:
            # 305546 USD = 512589.24 AUD | 314844.94 EUR | 215584.12 GBP | 3000000.00 NOK
            message = "%.2f %s" %(amount, code) + " = " + "%.2f %s" %(total_aud, "AUD") + " | " + "%.2f %s" %(total_eur, "EUR") + " | " + "%.2f %s" %(total_gbp, "GBP") + " | " + "%.2f %s" %(total_nok, "NOK")
        elif code == "AUD":
            message = "%.2f %s" % (amount, code) + " = "+ "%.2f %s" % (total_eur, "EUR") + " | " + "%.2f %s" % (total_gbp, "GBP") + " | " + "%.2f %s" % (total_nok, "NOK")
        elif code == "EUR":
            message = "%.2f %s" % (amount, code) + " = "+ "%.2f %s" % (total_aud, "AUD") + " | " + "%.2f %s" % (total_gbp, "GBP") + " | " + "%.2f %s" % (total_nok, "NOK")
        elif code == "GBP":
            message = "%.2f %s" % (amount, code) + " = "+ "%.2f %s" % (total_aud, "AUD") + " | " + "%.2f %s" % (total_eur, "EUR") + " | " + "%.2f %s" % (total_nok, "NOK")
        elif code == "NOK":
            message = "%.2f %s" % (amount, code) + " = "+ "%.2f %s" % (total_aud, "AUD") + " | " + "%.2f %s" % (total_eur, "EUR") + " | " + "%.2f %s" % (total_gbp, "GBP")


        modules.connection.send_message(message, i_medium, i_alias)
