__author__ = 'Djidiouf'

# Python built-in modules
import requests  # Install module: requests

# Third party modules
from bs4 import BeautifulSoup  # Install beautifulsoup4
import lxml  # Install lxml  # Used for parsing html

# Project modules
import modules.textalteration


def get_russian_price(i_string):

    title_requested = modules.textalteration.string_replace(i_string, " ", "+")

    # url = "http://www.allkeyshop.com/catalogue/search.php?q=%s&sort=nameAsc" % title_requested
    url = "https://www.allkeyshop.com/blog/catalogue/search-%s/sort-name-asc/" % title_requested
    webpage = requests.get(url, stream=True)
    soup = BeautifulSoup(webpage.text, 'lxml')

    # search_results = soup.select(".searchresults #table1 #tbody1 #tr4 #td5 #strong2")
    game_url = soup.select(".searchresults table tr:nth-of-type(2) td:nth-of-type(1) a")
    price = soup.select(".searchresults tr:nth-of-type(2) strong")

    store_url = game_url[0].get('href')
    store_price = price[0].get_text()
    tup_russian = (store_url, store_price)

    return tup_russian
