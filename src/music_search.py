import logging
import re
import requests

from src.database.db import DatabaseDriver

DEEZER_SEARCH = 'https://api.deezer.com/search?q='

def search_deezer(term):
    url = DEEZER_SEARCH + term
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("Received error HTTP code from Deezer API: {}".format(response.status_code))
    return response.json()

def parse_and_search_title(database_line_json):
    title = database_line_json['intvals']['worktitle']
    deezer_results = search_deezer(title)
    print(deezer_results)

if __name__ == '__main__':
    database = DatabaseDriver()
    try:
        print(database.search('cello'))
    finally:
        database.close()