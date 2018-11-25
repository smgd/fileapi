from flask import jsonify

class BaseException(Exception):
    status_code = 400
    message = 'Error'

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

class BadRequest(BaseException):
    message = 'Bad Request'
    status_code = 400

class FileNotFound(BaseException):
    message = 'File Not Found'
    status_code = 404