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
    ids = set()
    while start < size and iterations > 0:
        end = mm.find(END_OF_LINE, start)
        if end < start:
            break

        json_raw_line = mm[start:end].decode('utf-8')
        # print(json_raw_line)
        parse = json.loads(json_raw_line)
        id = parse['id']
        # print(parse)

        if id in ids:
            print('Already there: {}'.format(id))
            mm.move(start, end, size - end)
            # end -= (end - start)
        else:
            ids.add(id)

        start = end + 1
        iterations += 1

    mm.flush()
    mm.close()
    file.close()