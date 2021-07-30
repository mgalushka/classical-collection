import json
import logging
import mmap
import os
import re
import requests

DATABASE = '../db.imslp'

PATTERN = re.compile(b'cello', re.IGNORECASE)
END_OF_LINE = b'\n'

DEEZER_SEARCH = 'https://api.deezer.com/search?q='

def search_deezer(term):
    url = DEEZER_SEARCH + term
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("Received error HTTP code from Deezer API: {}".format(response.status_code))
    return response.json()

if __name__ == '__main__':
    size = os.stat(DATABASE).st_size
    f = open(DATABASE, "r+")
    mm = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)

    start = 0
    iterations = 1
    while start < size and iterations > 0:
        results = PATTERN.search(mm, start)
        if not results:
            break
        # print(mm[results.start():results.end()])
        rstart = results.start()
        rend = results.end()
        # print(rstart, rend)

        # PATTERN.search(mm, results.start() - 1000)
        line_start = mm.rfind(END_OF_LINE, 0, rstart)
        if line_start == -1:
            line_start = 0
        line_end = mm.find(END_OF_LINE, rend)
        # print(mm[line_start+1:line_end])
        # print('\n')
        line_json = json.loads(mm[line_start+1:line_end].decode('utf-8'))
        # print(line_json)

        title = line_json['intvals']['worktitle']
        deezer_results = search_deezer(title)
        print(deezer_results)

        start = line_end + 1
        iterations -= 1

    mm.flush()
    mm.close()
    f.close()
