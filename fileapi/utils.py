from flask import send_file, jsonify
import os
from fileapi import app
import hashlib

def get_hash_md5(file):
    m = hashlib.md5()

    while True:
        data = file.read(8192)
        if not data:
            break
        m.update(data)

    file.seek(0)

    return m.hexdigest()

def make_path(file_hash):
    try:
        os.mkdir(os.path.join(app.config['DIR'], file_hash[:2]))
    except:
        pass

    return os.path.join(app.config['DIR'], file_hash[:2], file_hash)

def existence(file_hash):
    path = os.path.join(app.config['DIR'], file_hash[:2], file_hash)
    return os.path.exists(path), path

def give_file(file_hash):
    file_status, path = existence(file_hash)

    if file_status:
        return send_file(path, as_attachment=True)
    else:
        return jsonify({'error': 'file_not_found'})

def remove_file(file_hash):
    file_status, path = existence(file_hash)
    
    if file_status:
        os.remove(path)

        try:
            os.rmdir(os.path.join(app.config['DIR'], file_hash[:2]))
        except:
            pass

        return jsonify({'you_have': 'deleted_file'})
    else:
        return 'file_not_found'

def save_file(posted_file):
    file_hash = get_hash_md5(posted_file)
    file_status, path = existence(file_hash)

    if not file_status:
        new_path = make_path(file_hash)
        posted_file.save(path)
        return jsonify({'you_have_uploaded': 'file', 'hash': file_hash})
    else:
return jsonify({'file_already': 'exists', 'hash': file_hash})