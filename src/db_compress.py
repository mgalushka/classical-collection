import json
import mmap
import os

# Do database file backup before running this script
from src.database.config import DATABASE

END_OF_LINE = b'\n'

if __name__ == '__main__':
    size = os.stat(DATABASE).st_size
    file = open(DATABASE)
    mm = mmap.mmap(file.fileno(), size, access=mmap.ACCESS_READ | mmap.ACCESS_WRITE)

    start = 0
    iterations = 10
    while start < size and iterations > 0:
        end = mm.find(END_OF_LINE, size)
        if end == -1:
            end = size

        parse = json.load(mm[start:end])
        print(parse)

        start = end + 1
        iterations += 1
