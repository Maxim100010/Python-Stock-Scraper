[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/maxim-fraňo)
![Version 1.0.1](https://img.shields.io/badge/Version%3A%201.0.1%20-%20%2307f207)
[![License MIT](https://img.shields.io/badge/License%3A%20MIT%20-%20%23fc0d05)](https://github.com/Maxim100010/Stock_Scraper_Python/blob/master/LICENSE)
<h1>Python Stock  Scraper</h1>
A web scraping tool used for getting analyst forecasts for stocks from US-based exchanges. Offers customizability, such as maximum closing price for stocks, or the ability to scrape with or without paid proxies.
<h2>Description</h2>
Fully Python3-based application for scraping stock tickers and analyst forecasts for stocks listed on the NYSE and NASDAQ stock exchanges. The application first scrapes ticker symbols from one website and then uses these tickers to query another website where the analyst forecast is found. Many stocks do not have an analyst forecast, in which case the query will return 404 and move to the next ticker. If a stock has a forecast, information from the forecast is extracted, primarily the future low price, as well as the average rating of the analysts who made the forecast. Lastly, after both tickers and forecasts are scraped, Excel and CSV files are created to help view the results of the scraping, as well as aid future scraping by for example not having to scrape tickers again or using already scraped forecast to only scrape stocks present in that forecast. <br>
<details>
<summary><h3>Technical Description</h3></summary>

Requirements can be found [here](https://github.com/Maxim100010/Stock_Scraper_Python/blob/master/requirements.txt)
<br><br>
<h4>Ticker scraping</h4>
The code works alongside a proprietary config file used to determine the output and methods used within the program. At the start of the execution, the config file is checked for correctness. In most of the classes, to access the config file, the library Configparser is used. Next, scraping of stock tickers begins, here the Requests and Beautifulsoup4 libraries are used. During this scrape, we go letter by letter until we get all the ticker symbols that start with that letter. Then, using bs4, we work with the HTML code to extract the ticker symbol and the closing price. Depending on our choice in the config file, the ticker will get added to the internal list of tickers as long as its closing price is below the specified amount. During this scrape, it is also possible to use paid proxies. I did not bother including free proxies here, given that it is only 26 queries, which is unlikely to get you blocked. <br><br>
<h4>Forecast scraping</h4>
Now, we should have a CSV file including all extracted tickers and their prices which meet the specified criteria set in the config file. From this CSV file, a list is populated, which is then used to query analyst forecasts. If the ticker that is being used to query has a forecast, the appropriate information is retrieved and another query is made to retrieve the ratings of the analysts who made the forecast. These methods again utilize Requests and bs4 libraries. As a result of this process, a final Excel file is created where the results can be found. Another CSV file is also made to aid in the speed of scraping by scraping only stocks that we know have a forecast.
<h4>Proxies</h4>
It is possible to use free proxies in this application or scrape with no proxy. When scraping Tickers, it is unlikely that a person will get blocked when using their own IP or a VPN. However during forecast scrape, given a large number of entries to scrape, the user will most likely get blocked within the first 100 queries. I have added the possibility of using free proxies. The ones I found did not make a difference between scraping with just a VPN but maybe there are some out there which are better. I am not versed enough in proxies to make free proxies or just scraping with a VPN work. If one wants to use free proxies, then they need to be in a JSON format with the keys 'ip' and 'port'<br> That is why I added the possibility of paid proxies. I personally used Oxylabs, which provides a link with credentials that can be easily inserted into the code, in this case through the use of the config file. I do not know if other providers use the same method. If not, then the code would need to be changed to fit your provider. With the paid proxies, the process goes from start to finish without an issue. With free proxies, whenever a code 429 is returned, the application exits.
<h4>Excel & CSV</h4>
One class is responsible for creating and reading Excel and CSV files. Here the libraries Openpyxl and Pandas are used.
</details>
<h3>Future improvements</h3>
The code itself could use refactoring, given that most likely all proper practices were not adhered to. However on the feature side, I would like to see the ability to start from or scrape only tickers starting with a specific letter, multithreading would increase the speed drastically, and GUI would make the app more user-friendly. Lastly, packaging the project so it can be used without an IDE would be a nice touch.
<h3>Disclaimer</h3>
I am by no means a profesional in Python. I chose Python for simplicity's sake, given that I knew I could output this application in a relatively short time. I have not worked on this application every day but only occasionally in my free time. Thus, there is the possibility of errors still being present, even though I tried testing all the possible cases.
<br><br>
When it comes to the use of the app itself if one finds themselves using the output of this app as investment advice, know that I am not liable for any loss arising from any investment based on any recommendation, forecast, or other information provided
<h2>How to use</h2>
Currently, the project has to be loaded in an IDE that supports Python Virtual Environment, for example, I used PyCharm, but VSCode should be able to be used as well. <br><br>
<b>Step-by-step guide</b><br><br>
<ol>
    <li>Open the project in your IDE of choice</li>
    <li>Adjust settings in configuration.ini to your preference (see next section)</li>
    <li>Run the main.py file</li>
    <li>Wait for the results</li>
</ol>
<b>Config file</b><br><br>
The config file serves as an accessible place for any customization of the program. The following are the possible options that can be changed.
<br><br>
<ul>
    <li>ExchangeToScan - Offers a choice between NYSE, NASDAQ, or both exchanges</li>
    <li>ClosingPriceLimit - Used for filtering stocks that will be scraped based on price i.e. If you want stocks whose last closing price was less than X</li>
    <li>LowToClosingDifference - Difference in percentage between the closing price and future low closing price</li>
    <li>AverageAnalystRating - Average rating of analysts who made the forecast, this value can be between 1 and 5</li>
    <li>TickersPaidProxy - Enable or disable usage of paid proxy for scraping ticker symbols</li>
    <li>ConsensusPaidProxy - Enable or disable usage of paid proxy for scraping consensus (forecast)</li>
    <li>PaidProxyLink - Link to paid proxies</li>
    <li>FreeProxyLink - Link to free proxies. If no free proxy link is provided, then no proxies are used</li>
    <li>FreshStart - Enable or disable scraping from scratch, which means scraping without the use of any pre-existing CSV files i.e. TickersPrices.csv</li>
</ul>
<br>
<h2>License</h2>
Distributed under the MIT license.
