from flask import Flask
import os

app = Flask(__name__)
app.config['DIR'] = os.path.join(os.getcwd(), 'storage')
print(app.config['DIR'])

from fileapi import daemon