from flask import Flask, render_template, request
from werkzeug.utils import redirect

from src.database.db import DatabaseDriver
from src.deezer.deezer import DeezerDriver

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
    app.logger.info(term)
    print(term)
    database = DatabaseDriver()
    try:
        results = database.search(term, terms_per_page=1000)
        app.logger.info(results)
    finally:
        database.close()
    return render_template('index.html', results=results)

@app.route('/deezer_search', methods=['GET', 'POST'])
def deezer_search():
    term = None
    if request.method == 'GET':
        term = request.args.get('term', '')
    if request.method == 'POST':
        term = request.form.get('term', '')

    if not term:
        return render_template('deezer.html', results=None)

    app.logger.info(term)
    deezer = DeezerDriver()
    results = deezer.search(term)
    app.logger.info(results)

    return render_template('deezer.html', results=results)