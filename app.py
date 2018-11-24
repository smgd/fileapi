from flask import Flask, url_for, send_file, request, jsonify, render_template
import hashlib
import os

app = Flask(__name__)
UPLOAD_DIR = '/home/soapman/Documents/code/py/fileapi/storage'
app.config['DIR'] = UPLOAD_DIR
file_base = []

def get_hash_md5(file):
    m = hashlib.md5()
    while True:
        data = file.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

def save_file(file):
    try:
        os.mkdir(app.config['DIR'] + '/' + file[:2])
    except:
        pass
    return os.path.join(app.config['DIR'], file[:2], file)

@app.route('/')
def home():
	return render_template('index.html')

# @app.route('/api', methods = ['GET'])

@app.route('/api/files', methods=['GET', 'POST', 'DELETE'])
def files():
    if request.method == 'GET':
        if not request.args:
            return jsonify(file_base)
        elif 'hash' in request.args:
            path = os.path.join(app.config['DIR'], request.args['hash'][:2], request.args['hash'])
            if os.path.exists(path):
            # print(path)
                return send_file(path, as_attachment=True)
            return jsonify({'you_better': 'than_most', 'you_can': 'download_file', 'hash': request.args['hash']})
    
    if request.method == 'POST':
        
        f = request.files['file']
        hash_filename = get_hash_md5(f)
        if hash_filename not in file_base:
            f.save(save_file(hash_filename))
            file_base.append(hash_filename)
            return jsonify({'you_have_uploaded': 'file', 'hash': hash_filename})
        else:
            return jsonify({'file_already': 'exists', 'hash': hash_filename})
    
    if request.method == 'DELETE':
        return jsonify({'you_cant': 'delete_files'})

if __name__ == '__main__':
    app.run()