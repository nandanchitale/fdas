import cv2
import os
from PIL import Image
import imutils

from io import BytesIO
import base64

haar_file = 'haarcascade_frontalface_default.xml'

# img sample size
(width, height) = (130, 100)

face_algo = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def detect():
    video = cv2.VideoCapture(0)

    address = "http://192.168.43.1:8080/video"
    video.open(address)

    while True:
        (_, im) = video.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_algo.detectMultiScale(gray, 1.3, 2)
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))

        cv2.imshow("test", frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows


    return True
