from flask import Flask, url_for, send_file, request, jsonify, render_template
import hashlib
import os

app = Flask(__name__)
UPLOAD_DIR = '/home/soapman/Documents/code/py/fileapi/storage'
app.config['DIR'] = UPLOAD_DIR

def get_hash_md5(file):
    m = hashlib.md5()
    while True:
        data = file.read(8192)
        if not data:
            break
        m.update(data)
    file.seek(0)
    return m.hexdigest()

def make_path(file):
    os.mkdir(app.config['DIR'] + '/' + file[:2])
    return os.path.join(app.config['DIR'], file[:2], file)

def existance(file_hash):
    path = os.path.join(app.config['DIR'], file_hash[:2], file_hash)
    return os.path.exists(path), path

def show_files():
    for root, subdirs, files in os.walk(app.config['DIR']):
        if files != []:
            for file in files:
                yield file

file_base = [file for file in show_files()]

@app.route('/')
@app.route('/api')
def home():
    return render_template('index.html')


@app.route('/api/files', methods=['GET', 'POST', 'DELETE'])
def files():
    if request.method == 'GET':
        if not request.args:
            return jsonify(file_base)
        elif 'hash' in request.args:
            file_status, path = existance(request.args['hash'])
            if file_status:
                return send_file(path, as_attachment=True)
            else:
                return jsonify({'error': 'file_not_found'})
    
    if request.method == 'POST':
        f = request.files['file']
        hash_filename = get_hash_md5(f)
        if hash_filename not in file_base:
            path = make_path(hash_filename)
            f.save(path)
            file_base.append(hash_filename)
            return jsonify({'you_have_uploaded': 'file', 'hash': hash_filename})
        else:
            return jsonify({'file_already': 'exists', 'hash': hash_filename})
    
    if request.method == 'DELETE':
        file = request.args['hash']
        os.remove(os.path.join(app.config['DIR'], file[:2], file))
        file_base.remove(file)
        try:
            os.rmdir(os.path.join(app.config['DIR'], file[:2]))
        except:
            pass
        return jsonify({'you_have': 'deleted_file'})



if __name__ == '__main__':
    app.run()