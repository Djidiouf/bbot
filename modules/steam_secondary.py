__author__ = 'Djidiouf'

# Python built-in modules
import urllib.request  # Open url request on website

# Third party modules
from bs4 import BeautifulSoup
import lxml  # Used for parsing html

# Project modules
import modules.textalteration


def get_russian_price(i_string):

    title_requested=modules.textalteration.string_replace(i_string, " ", "+")

    url = "http://www.allkeyshop.com/catalogue/search.php?q=%s&sort=nameAsc" % title_requested
    webpage = urllib.request.urlopen(url)
    # soup = BeautifulSoup(webpage.read(), 'html.parser')
    soup = BeautifulSoup(webpage.read(), 'lxml')

    #search_results = soup.select(".searchresults #table1 #tbody1 #tr4 #td5 #strong2")
    url = soup.select(".searchresults table tr:nth-of-type(2) td:nth-of-type(1) a")
    price = soup.select(".searchresults tr:nth-of-type(2) strong")

    store_url=url[0].get('href')
    store_price=price[0].get_text()
    tup_russian=(store_url, store_price)

    return tup_russian
