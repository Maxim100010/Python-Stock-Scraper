import requests as req
import json
import configparser

config = configparser.ConfigParser()
config.read('configuration.ini')

def createProxyList ():

    url = config['DEFAULT']['freeproxylink']

    result = req.get(url)

    json_data = json.loads(result.text)

    listOfProxies = []

    for entry in json_data['proxies']:
        tuple_of_proxies = ('http://' + str(entry['ip'] + ':' + str(entry['port'])), bool(entry['ssl']))
        listOfProxies.append(tuple_of_proxies)

    return listOfProxies
