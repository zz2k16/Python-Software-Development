"""Search Class creates basic structure for searching for any endpoint by capturing a
dictionary as input and encoding a url for the request to make an API call.
Subclasses that inherit this base class must define their own
parameter method and endpoint value."""
import requests
from urllib.parse import urlencode
from datetime import datetime
from News import API
from sys import platform


class Search:
    # initializer sets endpoint value. Subclasses must set this.
    def __init__(self, endpoint):
        self.endpoint = endpoint

    # encode dictionary is url
    def encode_params(self, params):
        return self.endpoint + urlencode(params, doseq=True)

    # request date from API using url
    def response(self, url):
        return requests.get(url=url, headers=API.headers).json()

    # helper method for date formatting to ISO UTC
    def date_formatter(self, date):
        print(platform)
        start = datetime.strptime(date,'%d/%m/%Y')
        tail = 'T00:00:00Z'
        start_utc = start.strftime('%Y-%m-%d')
        return start_utc + tail


#TODO improve request method with exception handling


if __name__ == '__main__':

    print(platform)
