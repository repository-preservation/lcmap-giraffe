""" Client for EarthExplorer MachineToMachine API """
import json
from operator import add
from functools import reduce
import requests


HOST = 'https://earthexplorer.usgs.gov/inventory/json/v/1.4.1'
def _api(endpoint, data=None):
    url = '{}/{}'.format(HOST, endpoint)
    body = {'jsonRequest': json.dumps(data)} if data else {}
    return requests.post(url, data=body).json().get('data')


def login(username='username', password='password'):
    return _api('login',
                {'username': username, 'password': password})


def search(token, dataset='ARD_TILE', start=1, limit=5e4):
    return _api('search',
                {'apiKey': token, 'datasetName': dataset, "sortOrder": "ASC",
                 'startingNumber': start, 'maxResults': limit})


def psearch(token, dataset='ARD_TILE', chunk=5e3, limit=5e4):
    limit = limit or search(token, dataset, limit=1).get('totalHits')
    return reduce(add,
                  [search(token, dataset, start=i+1, limit=chunk).get('results')
                   for i in range(0, limit, chunk)])
