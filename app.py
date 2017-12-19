from mgmt import COIN, format_sentence, get_payload
from flask import Flask, jsonify, send_from_directory, request
import json
import re

app = Flask(__name__, static_url_path='/web')

@app.route('/trainer')
def send_index():
    return send_from_directory('web', "index.html")

@app.route('/use')
def send_use():
    return send_from_directory('web', "user-input.html")

@app.route('/analyze')
def send_analyze():
    return send_from_directory('web', "analyze.html")

@app.route('/analyze-rss')
def rss():
    # ANALYZE ALL ARTICLES IN RSS FEED
	analyzed = list()
	for entry in COIN.articles:
	    analyzed += [ get_payload(entry)]
	# print analyzed
	return jsonify(analyzed)

@app.route('/analyze-text')
def text():
    # ANALYZE TEXT
	payload = get_payload(request.query_string.replace("%20", " "))
	return jsonify(payload)

@app.route('/get-rss')
def get_rss():
    # ANALYZE ALL ARTICLES IN RSS FEED
	articles = list()
	for entry in COIN.articles:
	    articles += [entry.to_dict()]
	# print analyzed
	return jsonify(articles)

@app.route('/label-rss', methods=['POST'])
def label():
    # ANALYZE ALL ARTICLES IN RSS FEED
	articles = list()
	for entry in COIN.articles:
	    articles += [entry]
	# print analyzed
	return jsonify(articles)

@app.route('/save-positive')
def save_positive():
	message = request.query_string.replace("%20", " ")
	with open('./data/positive_articles.txt', 'r+') as fh:
	    text = fh.read()
	    if re.search(r'(?m)^'+message, text):
	        return jsonify({"status":"Found"})
	    else:
	        fh.write(message+'\n')
	        return jsonify({"status":"added"})

	
@app.route('/save-negative')
def save_negative():
	message = request.query_string.replace("%20", " ")
	with open('./data/negative_articles.txt', 'r+') as fh:
	    text = fh.read()
	    if re.search(r'(?m)^'+message, text):
	        return jsonify({"status":"Found"})
	    else:
	        fh.write(message+'\n')
	        return jsonify({"status":"added"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21212)
    # app['debug'] = True 

