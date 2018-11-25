from flask import send_file, jsonify
import os
from fileapi import app
import hashlib
from fileapi.exceptions import FileNotFound

def get_hash_md5(file):
    """Return the md5 hashsum of the file"""
    hash_counter = hashlib.md5()

    while True:
        data = file.read(8192)
        if not data:
            break
        hash_counter.update(data)

    file.seek(0)

    return hash_counter.hexdigest()

def make_path(file_hash):
    """Create directory if needed and returns path for file"""
    try:
        os.mkdir(os.path.join(app.config['DIR'], file_hash[:2]))
    except:
        pass

    return os.path.join(app.config['DIR'], file_hash[:2], file_hash)

def existence(file_hash):
    """Check the existence of a file"""
    path = os.path.join(app.config['DIR'], file_hash[:2], file_hash)
    return os.path.exists(path), path

def give_file(file_hash):
    """Send file or error to user"""
    file_status, path = existence(file_hash)

    if file_status:
        return send_file(path, as_attachment=True)
    else:
        raise FileNotFound()

def remove_file(file_hash):
    """Remove file and directory if empty"""
    file_status, path = existence(file_hash)
    
    if file_status:
        os.remove(path)

        try:
            os.rmdir(os.path.join(app.config['DIR'], file_hash[:2]))
        except:
            pass

        return jsonify({'status_code': '200'})
    else:
        raise FileNotFound()

def save_file(posted_file):
    """Save file to storage"""
    file_hash = get_hash_md5(posted_file)
    file_status, path = existence(file_hash)

    if not file_status:
        new_path = make_path(file_hash)
        posted_file.save(path)
    
    return jsonify({'status_code': '200', 'hash': file_hash})