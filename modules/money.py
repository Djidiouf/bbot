__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website

# Project modules
import modules.connection
import modules.textalteration


def main(i_string, i_medium, i_alias=None):
    """
    Responds to a user that inputs "!money <number> <CODE1>:<CODE2>"
    API used: https://www.google.com/finance/converter

    :param i_string: a string with these elements: "<number> <CODE1>:<CODE2>"
    :print: parsed answer about money from the API
    """

    # divide a string in a tuple: 'str1', 'separator', 'str2'
    tuple_string = i_string.partition(' ')
    amount = tuple_string[0]
    codes = tuple_string[2]

    # amount needs to be int and not string
    amount = float(amount)

    # divide a string in a tuple: 'str1', 'separator', 'str2'
    list_currencies = modules.textalteration.string_split(codes, ":", " in ", " IN ", " ")
    code1 = list_currencies[0].upper()
    code2 = list_currencies[1].upper()

    url = 'https://finance.google.com/finance/converter?a=1&from=%s&to=%s' % (code1, code2)


    # Define where the results could be find and convert the split separator in byte.
    # Can't be simplified as a variable can't be called through bytes
    separator1 = '</div>\n&nbsp;\n<div id=currency_converter_result>1 %s = <span class=bld>' % code1  # Google
    separator1 = str.encode(separator1)  # Convert it in a byte type

    separator2 = ' %s</span>' % code2  # Google
    separator2 = str.encode(separator2)  # Convert it in a byte type

    webpage = urllib.request.urlopen(url)

    rate = float(webpage.read().split(separator1)[1].split(separator2)[0].strip())
    total = amount * rate
    # modules.connection.send_message('Rate: 1 %s = %.4f %s' % (code1, rate, code2))
    # modules.connection.send_message('%.2f %s = %.2f %s' % (amount, code1, total, code2))
    modules.connection.send_message('%.2f %s = %.2f %s' % (amount, code1, total, code2) + ' (1 %s = %.4f %s)' % (code1, rate, code2), i_medium, i_alias)
    webpage.close()
