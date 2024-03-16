import os
import re
import sys
import time
import configparser
from requests_ip_rotator import ApiGateway
import requests as req
from bs4 import BeautifulSoup as bs
import ExcelManipulator as em
import Proxies as px
from fake_useragent import UserAgent
import operator

proxy_counter = 0

config = configparser.ConfigParser()
config.read('configuration.ini')

def rotateProxy(list_of_proxies):
    global proxy_counter
    if proxy_counter + 1 == len(list_of_proxies):
        proxy_counter = -1
    proxies = {}
    proxy_counter += 1
    proxies['http'] = list_of_proxies[proxy_counter][0]
    if list_of_proxies[proxy_counter][1] == True: proxies['https'] = list_of_proxies[proxy_counter][0]

    return proxies

def extractDataFromHTML(result, result_ratings, tup):
    soup = bs(result.text, features='lxml')
    new_tuple = None
    if not 'n/a' in str(soup.find_all('td')[1]):
        low_price = str(soup.find_all('td')[1]).split('$', 1)[1].split('<', 1)[0]
        change = ((float(low_price) - float(tup[1])) / float(tup[1])) * 100
        rounded_change = round(change, 2)

        soup_ratings = bs(result_ratings.text, features='lxml')
        latest_analysts_rating = str(soup_ratings.find_all('div', {"class": "stars md"})[0]).split(':', 1)[1].split(';', 1)[0]

        if float(latest_analysts_rating) < float(config['DEFAULT']['AverageAnalystRating']):
            return new_tuple

        new_tuple = (
            tup[0], tup[1] + '$', low_price  + '$',
            str(rounded_change) + '%',
            latest_analysts_rating)
        print(new_tuple)
    return new_tuple

def scrapeConsensus(ListOfTickersAndPrices):

    url = 'https://stockanalysis.com/stocks/'

    TickerClosingLowChangeRatingList = []

    list_of_proxies = px.createProxyList()

    if len(list_of_proxies) == 0: sys.exit('No proxies found')

    print("Entries to scrape: " + str(len(ListOfTickersAndPrices)))

    rotation_counter = 0

    proxies = {}

    proxies['http'] = list_of_proxies[0][0]
    if list_of_proxies[0][1] == True: proxies['https'] = list_of_proxies[0][0]

    for tup in ListOfTickersAndPrices:
        if rotation_counter == 11:
            rotation_counter = 0
            proxies = rotateProxy(list_of_proxies)

        print('Current proxy: ' + str(proxies) + ' iteration ' + str(rotation_counter))
        print('Getting: ' + str(tup) + ' ' + str(iteration_counter) + '/' + str(len(ListOfTickersAndPrices)))
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

        if result.status_code == 200:
            while True:
                try:
                    headers = {
                        'User_Agent': str(UserAgent.random)
                    }

                    result_ratings = req.get(url + tup[0].lower() + '/ratings', proxies=proxies, headers=headers)
                    while True:
                        if result_ratings.status_code == 404 or result_ratings.status_code == 200:
                            break
                        proxies = rotateProxy(list_of_proxies)
                        print('Current proxy: ' + str(proxies) + ' iteration ' + str(rotation_counter))
                        headers = {
                            'User_Agent': str(UserAgent.random)
                        }
                        result_ratings = req.get(url + tup[0].lower() + '/ratings', headers=headers, proxies=proxies,
                                             timeout=3)
                        print(result_ratings.status_code)
                    if result_ratings.status_code == 404 or result_ratings.status_code == 200:
                        break
                except req.exceptions.ProxyError:
                    print('Proxy Error')
                    proxies = rotateProxy(list_of_proxies)
                except req.exceptions.Timeout:
                    print('Timed out')
                    proxies = rotateProxy(list_of_proxies)

        print(result.status_code)
        if result.status_code == 200:
            new_tuple = extractDataFromHTML(result, result_ratings, tup)
            if new_tuple != None:
                TickerClosingLowChangeRatingList.append(new_tuple)
        rotation_counter += 1
    return sorted(TickerClosingLowChangeRatingList, key=operator.itemgetter(3, 4), reverse=True)

def scrapeConsensusWithPaidProxies(ListOfTickersAndPrices):

    url = 'https://stockanalysis.com/stocks/'

    TickerClosingLowChangeRatingList = []

    proxies = {
        'http': config['DEFAULT']['paidproxylink'],
        'https': config['DEFAULT']['paidproxylink']
    }

    print("Entries to scrape: " + str(len(ListOfTickersAndPrices)))

    iteration_counter = 0

    for tup in ListOfTickersAndPrices:

        if iteration_counter == 75:
            break

        iteration_counter += 1

        print('Getting: ' + str(tup) + ' ' + str(iteration_counter) + '/' + str(len(ListOfTickersAndPrices)))

        while True:
            try:
                result = req.get(url + tup[0].lower() + '/forecast', proxies=proxies)
                if result.status_code == 200 or result.status_code == 404:
                    break
            except req.exceptions.ProxyError:
                print('Proxy Error')
        if result.status_code == 200:
            while True:
                try:
                    result_ratings = req.get(url + tup[0].lower() + '/ratings', proxies=proxies)
                    if result_ratings.status_code == 200 or result_ratings.status_code == 404:
                        break
                except req.exceptions.ProxyError:
                    print('Proxy Error')
        print(result.status_code)
        if result.status_code == 200:
            new_tuple = extractDataFromHTML(result, result_ratings, tup)
            if new_tuple != None:
                TickerClosingLowChangeRatingList.append(new_tuple)

    return sorted(TickerClosingLowChangeRatingList, key=lambda x: (float(x[3].split('%')[0]), float(x[4])), reverse=True)

em.createConsensusExcelSpreadsheet(scrapeConsensusWithPaidProxies(em.TickerCSVtoList()))