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
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment, Color
import operator


def createTickerExcelSpreadsheet (ticker_list):

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

def createConsensusExcelSpreadsheet (TickerClosingLowChangeRatingList):
    if os.path.isfile('Consensus.xlsx'):
        os.remove('Consensus.xlsx')

    wb = Workbook()
    ws = wb.active
    ws.title = 'Analyst Consensus'
    ws.merge_cells('A1:E1')

    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 35
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 50

    a1 = ws['A1']
    a1.value = 'Current Consensus from: ' + str(datetime.date.today())
    a1.font = Font(bold = True)
    a1.alignment = Alignment(horizontal='center')
    a1.fill = PatternFill("solid", fgColor="00C0C0C0")

    a2 = ws['A2']
    a2.value = 'Ticker'
    a2.font = Font(bold=True)
    a2.alignment = Alignment(horizontal='center')
    a2.fill = PatternFill("solid", fgColor="00C0C0C0")

    b2 = ws['B2']
    b2.value = 'Closing Price'
    b2.font = Font(bold=True)
    b2.alignment = Alignment(horizontal='center')
    b2.fill = PatternFill("solid", fgColor="00C0C0C0")

    c2 = ws['C2']
    c2.value = '12-month Forecasted LOW Price'
    c2.font = Font(bold=True)
    c2.alignment = Alignment(horizontal='center')
    c2.fill = PatternFill("solid", fgColor="00C0C0C0")

    d2 = ws['D2']
    d2.value = 'Percentual Change'
    d2.font = Font(bold=True)
    d2.alignment = Alignment(horizontal='center')
    d2.fill = PatternFill("solid", fgColor="00C0C0C0")

    e2 = ws['E2']
    e2.value = 'Rating of the Analysts Who Made The Forecast (0-5)'
    e2.font = Font(bold=True)
    e2.alignment = Alignment(horizontal='center')
    e2.fill = PatternFill("solid", fgColor="00C0C0C0")

    index = 3

    for tup in TickerClosingLowChangeRatingList:
        if '-' in tup[3]:
            color = '00FF0000'
        else:
            color = '0000FF00'
        ws['A' + str(index)] = tup[0]
        ws['A' + str(index)].fill = PatternFill("solid", fgColor=color)
        ws['B' + str(index)] = tup[1]
        ws['B' + str(index)].fill = PatternFill("solid", fgColor=color)
        ws['C' + str(index)] = tup[2]
        ws['C' + str(index)].fill = PatternFill("solid", fgColor=color)
        ws['D' + str(index)] = tup[3]
        ws['D' + str(index)].fill = PatternFill("solid", fgColor=color)
        ws['E' + str(index)] = tup[4]
        ws['E' + str(index)].fill = PatternFill("solid", fgColor=color)
        index += 1

    wb.save('Consensus.xlsx')

def createTickerCSV (ticker_list):
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

def TickerCSVtoList():

    df = pd.read_csv('TickersPrices.csv')

    data = df[['Ticker','Price']]

    ListOfTickersAndPrices = []

    for ind in data.index:
        ListOfTickersAndPrices.append((str(data['Ticker'][ind]), str(data['Price'][ind])))

    return ListOfTickersAndPrices


# list = [
#     ('AADI', '1.9$', '5.00$', '263.16%', ' 1.85'),
#     ('AAL', '14.64$', '11$', '-75.14%', ' 2.48')
# ]
#
# createConsensusExcelSpreadsheet(list)