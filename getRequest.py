# app.py
import sys
from scrapingNews import scrapeNews
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request
    else:
        person = app.config.get('person')
        numPages = app.config.get('numPages')
        message = scrapeNews(person, numPages, "True")
        return jsonify(message)  # serialize and use JSON headers

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('index.html')

if __name__ == '__main__':
    app.config['person'] = sys.argv[1]
    app.config['numPages'] = sys.argv[2]
	# run!
    app.run()
