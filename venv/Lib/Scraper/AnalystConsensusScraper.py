import os
import re
import time
from requests_ip_rotator import ApiGateway
import requests as req
from bs4 import BeautifulSoup as bs
import ExcelManipulator as em
import Proxies as px
import socket
from fake_useragent import UserAgent

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
        print('Getting: ' + str(tup))
        while True:
            try:
                headers = {
                    'User_Agent': str(UserAgent.random)
                }
                result = req.get(url + tup[0].lower() + '/forecast', headers=headers, proxies=proxies, timeout=3)
                while True:
                    if result.status_code == 404 or result.status_code == 200:
                        break
                    proxies = rotateProxy(list_of_proxies)
                    print('Current proxy: ' + str(proxies) + ' iteration ' + str(rotation_counter))
                    headers = {
                        'User_Agent': str(UserAgent.random)
                    }
                    result = req.get(url + tup[0].lower() + '/forecast', headers=headers, proxies=proxies, timeout=3)
                    print(result.status_code)
                if result.status_code == 404 or result.status_code == 200:
                    break
            except req.exceptions.ProxyError:
                proxies = rotateProxy(list_of_proxies)
                print('Proxy Error')
            except req.exceptions.Timeout:
                print('Timed out')
                proxies = rotateProxy(list_of_proxies)

        print(result.status_code)
        if result.status_code == 200:
            soup = bs(result.text, features='lxml')
            if not 'n/a' in str(soup.find_all('td')[1]):
                low_price = str(soup.find_all('td')[1]).split('$', 1)[1].split('<',1)[0]
                change = (float(low_price)/float(tup[1]))*100
                rounded_change = round(change, 2)
                new_tuple = (tup[0], tup[1], low_price, str(change)+'%' if tup[1] < low_price else '-' + str(change) + '%')
                print(new_tuple)
                TickerClosingLowChange.append(new_tuple)
        rotation_counter += 1
    return TickerClosingLowChange

def scrapeConsensusWithPaidProxies(ListOfTickersAndPrices):

    url = 'https://stockanalysis.com/stocks/'

    TickerClosingLowChange = []

    proxies = {
        'http': 'http://customer-scraperproxyuser:6AfKYJzVqq9Yz@pr.oxylabs.io:7777',
        'https': 'http://customer-scraperproxyuser:6AfKYJzVqq9Yz@pr.oxylabs.io:7777'
    }

    print("Entries to scrape: " + str(len(ListOfTickersAndPrices)))

    iteration_counter = 0

    for tup in ListOfTickersAndPrices:

        iteration_counter += 1

        print('Getting: ' + str(tup) + ' ' + str(iteration_counter) + '/' + str(len(ListOfTickersAndPrices)))

        while True:
            try:
                result = req.get(url + tup[0].lower() + '/forecast', proxies=proxies)
                if result.status_code == 200 or result.status_code == 404:
                    break
            except req.exceptions.ProxyError:
                print('Proxy Error')

        print(result.status_code)
        if result.status_code == 200:
            soup = bs(result.text, features='lxml')
            if not 'n/a' in str(soup.find_all('td')[1]):
                low_price = str(soup.find_all('td')[1]).split('$', 1)[1].split('<', 1)[0]
                change = (float(low_price) / float(tup[1])) * 100
                rounded_change = round(change, 2)
                new_tuple = (
                tup[0], tup[1], low_price, str(change) + '%' if tup[1] < low_price else '-' + str(change) + '%')
                print(new_tuple)
                TickerClosingLowChange.append(new_tuple)
    return TickerClosingLowChange



hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
print("Your Computer Name is:"+hostname)
print("Your Computer IP Address is:"+IPAddr)
print(scrapeConsensusWithPaidProxies(em.CSVtoList()))