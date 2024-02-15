import re
import string

import requests as req
from bs4 import BeautifulSoup as bs

def createTickerList ():

    alphabet = list(string.ascii_uppercase)

    #NYSE URL
    URL_NY = "https://eoddata.com/stocklist/NYSE/"

    #NASDAQ URL
    URL_NA = "https://eoddata.com/stocklist/NASDAQ/"

    ticker_list = []

    for letter in alphabet:
        result = req.get(URL_NA + letter + ".htm")
        soup = bs(result.text, features="lxml")
        for tr in soup.find_all("tr", onclick = re.compile("/stockquote/NASDAQ/")):
            ticker_list.append(str(tr).split("NASDAQ/", 1)[1].split(".", 1)[0])
    return

createTickerList()