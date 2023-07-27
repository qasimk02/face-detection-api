from flask import Flask, jsonify, request
import cv2
import urllib.request
import socket

app = Flask(__name__)


def detect_faces(image_url):
    # Perform face detection
    urllib.request.urlretrieve(image_url, 'image.jpg')
    image = cv2.imread('image.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Extract face coordinates
    face_coordinates = {"outputs": []}
    for (x, y, w, h) in faces:
        face_coordinates["outputs"].append(
            {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)})

    return face_coordinates


@app.route('/detect_faces', methods=['POST'])
def stream_faces():
    image_url = request.json['image_url']
    face_coordinates = detect_faces(image_url)
    return jsonify(face_coordinates)


if __name__ == "__main__":
    app.debug = True
    IPAddr = socket.gethostbyname(socket.gethostname())
    app.run(host=IPAddr, port=5000)
