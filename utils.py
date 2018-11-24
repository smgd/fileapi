from flask import Flask, url_for, send_file, request, jsonify, render_template
import os

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
    try:
        os.mkdir(app.config['DIR'] + '/' + file[:2])
    except:
        pass
    return os.path.join(app.config['DIR'], file[:2], file)

def existance(file_hash):
    path = os.path.join(app.config['DIR'], file_hash[:2], file_hash)
    return os.path.exists(path), path

def show_files():
    for root, subdirs, files in os.walk(app.config['DIR']):
        if files != []:
            for file in files:
                yield file

def give_file(file_hash)
    file_status, path = existance(file_hash)
        if file_status:
            return send_file(path, as_attachment=True)
        else:
            return jsonify({'error': 'file_not_found'})

def remove_file(file):
    if file in file_base:
        os.remove(os.path.join(app.config['DIR'], file[:2], file))
        file_base.remove(file)
        try:
            os.rmdir(os.path.join(app.config['DIR'], file[:2]))
        except:
            pass
        return jsonify({'you_have': 'deleted_file'})
    else:
        return 'file_not_found'

def save_file(posted_file):
    hash_filename = get_hash_md5(posted_file)
        if hash_filename not in file_base:
            path = make_path(hash_filename)
            posted_file.save(path)
            file_base.append(hash_filename)
            return jsonify({'you_have_uploaded': 'file', 'hash': hash_filename})
        else:
            return jsonify({'file_already': 'exists', 'hash': hash_filename})


file_base = [file for file in show_files()]