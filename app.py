from flask import Flask, url_for, send_file, request, jsonify
import hashlib

app = Flask(__name__)

def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

@app.route('/')
def home():
	return jsonify({'bla':'bla'})

@app.route('/files')
def files():
	return jsonify({'you_should': 'download_files'})

if __name__ == '__main__':
    app.run()