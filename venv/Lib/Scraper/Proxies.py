import requests as req
import json
import configparser

config = configparser.ConfigParser()
config.read('configuration.ini')

def createProxyList ():

    url = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&country=AT,BE,CZ,EE,FR,DE,NL,GB&anonymity=elite&timeout=1550&proxy_format=ipport&format=json'

    result = req.get(url)

    json_data = json.loads(result.text)

    listOfProxies = []

    for entry in json_data['proxies']:
        tuple_of_proxies = ('http://' + str(entry['ip'] + ':' + str(entry['port'])), bool(entry['ssl']))
        listOfProxies.append(tuple_of_proxies)

    return listOfProxies

print(createProxyList())
