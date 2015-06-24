from flask import jsonify

class InvalidUsage(Exception):
    status = 400

    def __init__(self, message, code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if code is not None:
            self.status= code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv