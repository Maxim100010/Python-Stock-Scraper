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


def createExcelSpreadsheet (ticker_list):

    if os.path.isfile('TickersPrices.xlsx'):
        wb = load_workbook(filename='TickersPrices.xlsx')
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = 'Tickers And Closing Prices'
        ws['A1'] = 'Current Tickers and prices from ' + str(datetime.date.today())
        ws['A2'] = 'Currently applied filters'
        ws['A3'] = 'Exchange: ' + config['DEFAULT']['exchangetoscan'].upper()
        ws['A4'] = 'Closing price limit: ' + config['DEFAULT']['closingpricelimit']
        ws['A5'] = 'Ticker'
        ws['B5'] = 'Price'

    index = 6
    for tup in ticker_list:
        ws['A' + str(index)] = tup[0]
        ws['B' + str(index)] = tup[1]
        index += 1

    wb.save('TickersPrices.xlsx')

def createCSV (ticker_list):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Data'

    ws['A1'] = 'Ticker'
    ws['B1'] = 'Price'

    index = 2
    for tup in ticker_list:
        ws['A' + str(index)] = tup[0]
        ws['B' + str(index)] = tup[1]
        index += 1

    wb.save('Temp.xlsx')

    read_file = pd.read_excel('Temp.xlsx')

    read_file.to_csv('TickersPrices.csv')

    os.remove('Temp.xlsx')

def CSVtoList():

    df = pd.read_csv('TickersPrices.csv')

    data = df[['Ticker','Price']]

    ListOfTickersAndPrices = []

    for ind in data.index:
        ListOfTickersAndPrices.append((str(data['Ticker'][ind]), str(data['Price'][ind])))

    return ListOfTickersAndPrices
