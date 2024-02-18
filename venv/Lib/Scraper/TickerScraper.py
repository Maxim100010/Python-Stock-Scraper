import datetime
import re
import string
import time
import configparser
import requests as req
import os
import os.path
import pandas as pd
import pyarrow
from bs4 import BeautifulSoup as bs
from openpyxl import Workbook
from openpyxl import load_workbook
import ExcelManipulator as em

config = configparser.ConfigParser()
config.read('configuration.ini')

def createTickerList (ExchangeToScan, ClosingPriceLimit):

    alphabet = list(string.ascii_uppercase)

    #NYSE URL
    URL_NY = "https://eoddata.com/stocklist/NYSE/" # Takes around 152 seconds

    #NASDAQ URL
    URL_NA = "https://eoddata.com/stocklist/NASDAQ/" #Takes around 153 seconds

    ticker_list = []

    #Decide which exchange to scan depending on config file
    if ExchangeToScan == 'both':
        ticker_list.extend(runNYSEscrape(alphabet, ticker_list, URL_NY, ClosingPriceLimit))
        ticker_list.extend(runNASDAQscrape(alphabet, ticker_list, URL_NA, ClosingPriceLimit))
    elif ExchangeToScan == 'nasdaq':
        ticker_list = runNASDAQscrape(alphabet, ticker_list, URL_NA, ClosingPriceLimit)
    elif ExchangeToScan == 'nyse':
        ticker_list = runNYSEscrape(alphabet, ticker_list, URL_NY, ClosingPriceLimit)
    else:
        print('Error, ExchangeToScan variable did not match any case')

    print("Finished in: " + str(time.perf_counter()))

    return ticker_list

#Scrape NASDAQ listed stocks under desired closing price limit
def runNASDAQscrape (alphabet, ticker_list, URL_NA, closing_price_limit):
    for letter in alphabet:
        #Open URL
        result = req.get(URL_NA + letter + ".htm")
        #Parse HTML
        soup = bs(result.text, features="lxml")
        #For all HTML 'tr' tags extract ticker and price
        for tr in soup.find_all("tr", onclick = re.compile("/stockquote/NASDAQ/")):
            ticker = str(tr).split("NASDAQ/", 1)[1].split(".", 1)[0]
            closing_price = float(str(tr.td.next_sibling.next_sibling.next_sibling.next_sibling).split(">", 1)[1].split("<", 1)[0].replace(",", "."))
            if closing_price < float(closing_price_limit):
                ticker_closingprice_tuple = (ticker, closing_price)
                ticker_list.append(ticker_closingprice_tuple)

    return ticker_list

#Scrape NYSE listed stocks under desired closing price limit
def runNYSEscrape (alphabet, ticker_list, URL_NY, closing_price_limit):
    for letter in alphabet:
        #Open URL
        result = req.get(URL_NY + letter + ".htm")
        #Parse HTML
        soup = bs(result.text, features="lxml")
        #For all HTML 'tr' tags extract ticker and price
        for tr in soup.find_all("tr", onclick = re.compile("/stockquote/NYSE/")):
            ticker = str(tr).split("NYSE/", 1)[1].split(".", 1)[0]
            closing_price = float(
                str(tr.td.next_sibling.next_sibling.next_sibling.next_sibling).split(">", 1)[1].split("<", 1)[
                    0].replace(",", "."))
            if closing_price < float(closing_price_limit):
                ticker_closingprice_tuple = (ticker, closing_price)
                ticker_list.append(ticker_closingprice_tuple)

    return ticker_list




em.createCSV(createTickerList(config['DEFAULT']['exchangetoscan'], config['DEFAULT']['closingpricelimit']))
#createExcelSpreadsheet(createTickerList(config['DEFAULT']['exchangetoscan'], config['DEFAULT']['closingpricelimit']))
#print(createTickerList(config['DEFAULT']['exchangetoscan'], config['DEFAULT']['closingpricelimit']))