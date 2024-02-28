import os
import re
import time
from requests_ip_rotator import ApiGateway
import requests as req
from bs4 import BeautifulSoup as bs
import ExcelManipulator as em
import Proxies as px

proxy_counter = 0

def rotateProxy(list_of_proxies):
    global proxy_counter
    if proxy_counter + 1 == len(list_of_proxies):
        proxy_counter = -1
    proxies = {}
    proxy_counter += 1
    proxies['http'] = list_of_proxies[proxy_counter][0]
    if list_of_proxies[proxy_counter][1] == True: proxies['https'] = list_of_proxies[proxy_counter][0]

    return proxies

def scrapeConsensus(ListOfTickersAndPrices):

    url = 'https://stockanalysis.com/stocks/'

    TickerClosingLowChange = []

    list_of_proxies = px.createProxyList()

    rotation_counter = 0

    proxies = {}

    proxies['http'] = list_of_proxies[0][0]
    if list_of_proxies[0][1] == True: proxies['https'] = list_of_proxies[0][0]

    for tup in ListOfTickersAndPrices:
        if rotation_counter == 11:
            rotation_counter = 0
            proxies = rotateProxy(list_of_proxies)

        print('Current proxy: ' + str(proxies) + ' iteration ' + str(rotation_counter))
        try:
            result = req.get(url + tup[0].lower() + '/forecast', proxies=proxies, timeout=3)
        except req.exceptions.ProxyError:
            proxies = rotateProxy(list_of_proxies)
            print('Proxy Error')
        except req.exceptions.Timeout:
            print('Timed out')
            proxies = rotateProxy(list_of_proxies)

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