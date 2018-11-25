from flask import Flask
import os

app = Flask(__name__)
app.config['DIR'] = os.path.join(os.getcwd(), 'storage')

from fileapi import daemon