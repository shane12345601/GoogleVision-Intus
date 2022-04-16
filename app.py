import os
import io
from urllib import response
import flask
from google.cloud import vision
from google.cloud.vision_v1 import types
from flask import Flask
from flask_cors import CORS
import json

from requests import request

app = Flask(__name__)
CORS(app)
app.config['GOOGLE_APPLICATION_CREDENTIALS'] = "ServiceAccountToken.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "ServiceAccountToken.json"

@app.route('/')
def index():
    return "Intus OCR is Running!"

@app.route('/ocr/<url>')
def ocr(url):
    uri = url

    if 'url' in flask.request.args:
        uri = flask.request.args.get('url')
        client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image)

        texts = response.text_annotations

        alltext = (texts[0].description).split("\n")

        return json.dumps(alltext)

    return uri

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
