"""
A thin HTTP wrapper around the functionality in aaaas.image.
"""

from flask import Flask, abort, jsonify, request
from . import image

MAX_ASCII_DIMENSIONS = (128, 128)
MAX_IMAGE_SIZE_MB = 1

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_IMAGE_SIZE_MB * 1024 * 1024

####################

@app.route('/')
def index():
    return 'OK'

####################

def _uploaded_image():
    try:
        return request.files['image']
    except KeyError:
        abort(400, 'missing `image` file')

def _asciify(f):
    try:
        invert_colors = bool(request.args['invert'])
    except KeyError:
        invert_colors = False

    try:
        return image.to_ascii(f,
                              max_size=MAX_ASCII_DIMENSIONS,
                              invert_colors=invert_colors)
    except OSError:
        abort(400, 'invalid image')

def _respond(s):
    try:
        json = request.headers['accept'] == 'application/json'
    except KeyError:
        json = False
    if json:
        resp = app.make_response(jsonify({'ascii': s.split('\n')}))
        resp.headers['mimetype'] = 'application/json'
    else:
        resp = app.make_response(s)
        resp.headers['mimetype'] = 'text/plain'
    return resp

@app.route('/images', methods=['POST'])
def post_image():
    return _respond(_asciify(_uploaded_image()))
