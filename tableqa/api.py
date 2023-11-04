# -*- coding: utf-8 -*-

from urllib.request import urlopen

from flask import Flask, json, request, abort, jsonify
from werkzeug.exceptions import HTTPException

from .tableqa import TableQA
from .pdfparser import PDFParser

app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False
json.provider.DefaultJSONProvider.compact = True


@app.route('/tables', methods=['POST'])
def parse_tables():
    data = request.get_json()
    if 'file' not in data:
        abort(400, description='file is required')

    # Handle the file in data URLs format.
    with urlopen(data['file']) as file:
        bytes = file.read()

    with PDFParser(bytes) as p:
        tables = p.parse_tables()
    return jsonify({'tables': tables})


@app.route('/texts', methods=['POST'])
def parse_text():
    data = request.get_json()
    if 'file' not in data:
        abort(400, description='file is required')

    # Handle the file in data URLs format.
    with urlopen(data['file']) as file:
        bytes = file.read()

    with PDFParser(bytes) as p:
        text = p.parse_text()
    return jsonify({'text': text})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if 'tables' not in data:
        abort(400, description='tables is required')
    if 'question' not in data:
        abort(400, description='question is required')

    tables = data['tables']
    question = data['question']

    qa = TableQA(tables)
    answer = qa.chat(question)
    return jsonify(dict(answer=answer))


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify(error=e.description), e.code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
