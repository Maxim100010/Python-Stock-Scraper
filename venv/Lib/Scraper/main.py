import Scrapers.TickerScraper as tickerscraper
import ExcelCsvFiles.ExcelManipulator as excelmanipulator
import Scrapers.AnalystConsensusScraper as consensusscraper
import configparser
import os

config = configparser.ConfigParser()
config.read('configuration.ini')

print('Starting config validation...')
config_as_list = list(config['DEFAULT'].items())

exchange = config_as_list[0][1]
if(exchange.upper() not in ['NASDAQ', 'NYSE', 'BOTH']):
    raise Exception('Exchange has to be of values: NASDAQ, NYSE, or BOTH')

if(int(config_as_list[1][1]) < 1):
    raise Exception('Closing price limit can only be a non-negative non-zero number')

if(int(config_as_list[2][1]) < 1):
    raise Exception('Low to closing difference can only be a non-negative non-zero number')

if(int(config_as_list[3][1]) < 1 or int(config_as_list[3][1]) > 5):
    raise Exception('Average analyst rating must be at least one and less or equal to five')

if(config_as_list[4][1].lower() not in ['true', 'false']):
    raise Exception('Tickers paid proxy can either be true or false')

if(config_as_list[5][1].lower() not in ['true', 'false']):
    raise Exception('Consensus paid proxy can either be true or false')

if((config_as_list[4][1] == 'true' or config_as_list[5][1] == 'true') and config_as_list[6][1] == ''):
    raise Exception('If paid proxy scraping is enabled, a link to paid proxies must be provided')

if((config_as_list[4][1] == 'false' or config_as_list[5][1] == 'false') and config_as_list[7][1] == ''):
    raise Exception('If free proxy scraping is enabled, a link to free proxies must be provided')

if(config_as_list[8][1].lower() not in ['true', 'false']):
    raise Exception('Fresh start can either be true or false')

print('Current Settings')
print('------------------------------')
for key, value in config['DEFAULT'].items():
    print(f"{key}: {value}")
print('------------------------------')

if (config['DEFAULT']['freshstart'] == 'true'):

    #Create internal list of tickers from exchanges selected in config
    print('Starting Ticker Scrape...')
    ticker_list = tickerscraper.createTickerList(config['DEFAULT']['exchangetoscan'], config['DEFAULT']['closingpricelimit'])
    #Create excel file of tickers
    print('Starting Ticker Excel Creation...')
    excelmanipulator.createTickerExcelSpreadsheet(ticker_list)
    #Create CSV of tickers
    print('Starting Ticker CSV Creation...')
    excelmanipulator.createTickerCSV(ticker_list)
    #Scrape consensus depending on choice of proxies
    print('Starting Consensus Scrape...')
    if (config['DEFAULT']['consensuspaidproxy'] == 'true'):
        consensus = consensusscraper.scrapeConsensusWithPaidProxies(excelmanipulator.TickerCSVtoList())
    else:
        consensus = consensusscraper.scrapeConsensus(excelmanipulator.TickerCSVtoList())
    #Create excel file for the scraped consensus
    print('Starting Consensus Excel Creation...')
    excelmanipulator.createConsensusExcelSpreadsheet(consensus)
    #Create CSV file for scraped consensus for future scraping use
    print('Starting Consensus CSV Creation...')
    excelmanipulator.createTickersFromConsensusCSV(consensus)
    print('FINISHED SUCCESSFULLY')

else:

    # Use previously scraped consensus to scrape only those stocks again if file exists
    if os.path.isfile('ExcelCsvFiles/TickersPricesFromConsensus.csv'):
        print('Previous consensus file found, using this instead of full ticker price list')
        if (config['DEFAULT']['consensuspaidproxy'] == 'true'):
            consensus = consensusscraper.scrapeConsensusWithPaidProxies(excelmanipulator.TickersFromConsesusCSVtoList())
        else:
            consensus = consensusscraper.scrapeConsensus(excelmanipulator.TickersFromConsesusCSVtoList())
    else:
        # Otherwise, create internal list of tickers from exchanges selected in config
        if not os.path.isfile('ExcelCsvFiles/TickersPrices'+config['DEFAULT']['exchangetoscan']+'.xlsx'):
            print('Starting Ticker Scrape...')
            ticker_list = tickerscraper.createTickerList(config['DEFAULT']['exchangetoscan'],
                                                     config['DEFAULT']['closingpricelimit'])
            # Create excel file of tickers
            print('Starting Ticker Excel Creation...')
            excelmanipulator.createTickerExcelSpreadsheet(ticker_list)
            # Create CSV of tickers
            print('Starting Ticker CSV Creation...')
            excelmanipulator.createTickerCSV(ticker_list)
        else:
            print('Tickers and prices CSV for exchange '+config['DEFAULT']['exchangetoscan']+' already exists. Continuing...')
        # Scrape consensus depending on choice of proxies
        print('Starting Consensus Scrape...')
        if (config['DEFAULT']['consensuspaidproxy'] == 'true'):
            consensus = consensusscraper.scrapeConsensusWithPaidProxies(excelmanipulator.TickerCSVtoList())
        else:
            consensus = consensusscraper.scrapeConsensus(excelmanipulator.TickerCSVtoList())
    # Create excel file for the scraped consensus
    print('Starting Consensus Excel Creation...')
    excelmanipulator.createConsensusExcelSpreadsheet(consensus)
    # Create CSV file for scraped consensus for future scraping use
    print('Starting Consensus CSV Creation...')
    excelmanipulator.createTickersFromConsensusCSV(consensus)
    print('FINISHED SUCCESSFULLY')

