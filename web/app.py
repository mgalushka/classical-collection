# import logging
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from src.database.db import DatabaseDriver

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html', results=[])

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return redirect('/')
    app.logger.warning(request.args)
    term = request.form.get('term', '')
    app.logger.warning(term)
    print(term)
    database = DatabaseDriver()
    results = []
    try:
        results = database.search(term)
        app.logger.warning(results)
    finally:
        database.close()
    return render_template('index.html', results=results)