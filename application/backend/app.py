from flask import Flask, request
from flask_cors import CORS

from cv2 import cv2 as cv
import numpy as np
import base64

from algorithm import keyboard_detection

app = Flask(__name__)
CORS(app)


@app.route("/")
def root():
    return "<p>hello, world</p>"


@app.route("/edge-coordinates", methods=["POST"])
def getEdgeCoordinates():
    jsonRequest = request.json

    if jsonRequest is None:
        return {"error", "No data received"}, 400

    imageURI: str = jsonRequest["image"]

    if imageURI is None:
        return {"error", "No image data received"}, 400

    imageBase64 = imageURI.split(",")[1]

    imageArray = np.frombuffer(base64.b64decode(imageBase64), np.uint8)
    keyboardImage = cv.imdecode(imageArray, cv.IMREAD_COLOR)

    try:
        edgeCoordinates = keyboard_detection.getContourPointsFromImage(keyboardImage)
    except:
        return {"error": "Failure in getting edge coordinates"}, 500

    return {"coordinates": edgeCoordinates}
