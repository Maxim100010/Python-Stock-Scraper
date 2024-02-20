import os
import re
import time
from requests_ip_rotator import ApiGateway
import requests as req
from bs4 import BeautifulSoup as bs
import ExcelManipulator as em
import Proxies as px

def scrapeConsensus (ListOfTickersAndPrices):

    url = 'https://stockanalysis.com/stocks/'

    TickerClosingLowChange = []

    #list_of_proxies = px.createProxyList()

    rotation_counter = 0

    proxy_counter = 0

    proxies = {
        "http": 'http://195.90.216.75:8889',
        "https": 'http://3.126.135.206:8080'
    }

    for tup in ListOfTickersAndPrices:
        # if rotation_counter == 50:
        #     proxy_counter += 1
        #     proxies = {
        #         "http": list_of_proxies[proxy_counter],
        #         "https": list_of_proxies[proxy_counter]
        #     }
        print('Current proxy: ' + str(proxies) + ' iteration ' + str(rotation_counter))
        result = req.get(url + tup[0].lower() + '/forecast', proxies=proxies)
        print(result.status_code)
        if result.status_code == 200:
            print(tup)
            soup = bs(result.text, features='lxml')
            if not 'n/a' in str(soup.find_all('td')[1]):
                low_price = str(soup.find_all('td')[1]).split('$', 1)[1].split('<',1)[0]
                change = (float(low_price)/float(tup[1]))*100
                new_tuple = (tup[0], tup[1], low_price, str(change)+'%')
                TickerClosingLowChange.append(new_tuple)
        rotation_counter += 1
    return TickerClosingLowChange

print(scrapeConsensus(em.CSVtoList()))