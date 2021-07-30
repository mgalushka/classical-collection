import json
import logging
import requests

DATABASE = '../db.imslp'

URL = 'https://imslp.org/imslpscripts/API.ISCR.php?account=worklist/disclaimer=accepted/sort=id/type=2/start='
MAX_PAGE = 1000

if __name__ == '__main__':

    for start in range(0, MAX_PAGE):
        url = URL + str(start)
        response = requests.get(url)
        if response.status_code != 200:
            logging.error("End of stream, received error HTTP code: {}".format(response.status_code))
            break
        page = response.json()
        with open(DATABASE, 'a') as file:
            for key, value in page.items():
                json_line = json.dumps(value)
                file.write(json_line)
                file.write('\n')