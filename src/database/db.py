import json
import logging
import mmap
import os
import re

from .config import DATABASE

class DatabaseDriver:
    END_OF_LINE = b'\n'

    def __init__(self):
        self.is_opened = False
        self.size = -1
        self.file = None
        self.mmap = None
        self.open()

    def open(self):
        if not self.is_opened:
            self.size = os.stat(DATABASE).st_size
            self.file = open(DATABASE, "r+")
            self.mmap = mmap.mmap(self.file.fileno(), self.size, access=mmap.ACCESS_READ)
            self.is_opened = True

    def search(self, term, terms_per_page=10):
        self.open()
        pattern = re.compile(bytes('{term}'.format(term=term), 'utf-8'), re.IGNORECASE)
        start = 0
        iterations = terms_per_page
        found_results = []
        while start < self.size and iterations > 0:
            results = pattern.search(self.mmap, start)
            if not results:
                break
            rstart = results.start()
            rend = results.end()
            logging.info('Found hit for search term: {term} -> {value}, start={start}, end={end}'.format(
                term=term,
                value=self.mmap[rstart:rend],
                start=rstart,
                end=rend,
            ))

            line_start = self.mmap.rfind(self.END_OF_LINE, 0, rstart)
            if line_start == -1:
                line_start = 0
            line_end = self.mmap.find(self.END_OF_LINE, rend)

            json_raw_line = self.mmap[line_start+1:line_end].decode('utf-8')

            logging.info('Found matching full JSON line for search term: {term}: \n{value}\n, start={start}, end={end}'.format(
                term=term,
                value=json_raw_line ,
                start=line_start,
                end=line_end,
            ))
            line_parsed_json = json.loads(json_raw_line)
            found_results.append(line_parsed_json)

            start = line_end + 1
            iterations -= 1
        return found_results

    def close(self):
        self.mmap.flush()
        self.mmap.close()
        self.file.close()