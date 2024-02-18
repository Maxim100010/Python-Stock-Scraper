import os
import re
import time

import requests as req
from bs4 import BeautifulSoup as bs
import ExcelManipulator as em

def scrapeConsensus (ListOfTickersAndPrices):

    url = 'https://stockanalysis.com/stocks/'

    TickerClosingLowChange = []

    for tup in ListOfTickersAndPrices:
        time.sleep(0.5)
        result = req.get(url + tup[0].lower() + '/forecast')
        print(result.status_code)
        if result.status_code == 200:
            print(tup)
            soup = bs(result.text, features='lxml')
            if not 'n/a' in str(soup.find_all('td')[1]):
                low_price = str(soup.find_all('td')[1]).split('$', 1)[1].split('<',1)[0]
                change = (float(low_price)/float(tup[1]))*100
                new_tuple = (tup[0], tup[1], low_price, str(change)+'%')
                TickerClosingLowChange.append(new_tuple)

    return TickerClosingLowChange

print(scrapeConsensus(em.CSVtoList()))