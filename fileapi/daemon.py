from flask import Flask, send_file, request, jsonify, render_template, abort
import os

from fileapi import utils, app
from fileapi.exceptions import BadRequest, FileNotFound

@app.route('/')
@app.route('/api')
def home():
    return render_template('index.html')

@app.errorhandler(FileNotFound)
@app.errorhandler(BadRequest)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    response.message = error.message
    return response

@app.route('/api/files', methods=['GET', 'POST', 'DELETE'])
def files():
    if request.method == 'POST':
        return utils.save_file(request.files['file'])
    elif 'hash' in request.args:
        if request.method == 'GET':
            return utils.give_file(request.args['hash'])
        if request.method == 'DELETE':
            return utils.remove_file(request.args['hash'])
    else:
        raise BadRequest()