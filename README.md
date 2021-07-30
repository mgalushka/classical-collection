# Storage

We will store databse of records fetched from imslp.org into file in the format:
Every line is json object
This allows to search this file through regex.

# API
See: https://imslp.org/wiki/IMSLP:API

# Retrieval
1. mmap file and regexp.
2. find previous \n and next \n and parse record as json
3. search deezer API

# Music API
See: https://developers.deezer.com/api/explorer?url=search%3Fq%3Deminem



