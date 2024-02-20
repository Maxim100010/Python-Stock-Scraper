import requests as req
import json
import configparser

config = configparser.ConfigParser()
config.read('configuration.ini')

def createProxyList ():

    url = config['DEFAULT']['proxies']

    result = req.get(url)

    json_data = json.loads(result.text)

    listOfProxies = []

    for entry in json_data['data']:
        proxy_string =  'socks5://' + entry['ip'] + ':' + entry['port']
        listOfProxies.append(proxy_string)

    return listOfProxies
