from flask import Flask, url_for, send_file, request, jsonify, render_template
import os
from src import utils, app

@app.route('/')
@app.route('/api')
def home():
    return render_template('index.html')

@app.route('/api/files', methods=['GET', 'POST', 'DELETE'])
def files():
    if request.method == 'POST':
        return utils.save_file(request.files['file'])
    elif request.args['hash']:
        if request.method == 'GET':
            return utils.give_file(request.args['hash'])
        if request.method == 'DELETE':
            return utils.remove_file(request.args['hash'])
    else:
return 'wrong_request'