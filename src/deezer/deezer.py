import logging
import requests

class DeezerDriver:
    DEEZER_SEARCH = 'https://api.deezer.com/search?q='

    def __init__(self):
        pass

    def search(self, term):
        url = self.DEEZER_SEARCH + term
        response = requests.get(url)
        if response.status_code != 200:
            logging.error("Received error HTTP code from Deezer API: {}".format(response.status_code))
        return response.json()
