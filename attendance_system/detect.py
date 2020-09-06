import cv2, os 
from fdas.settings import MEDIA_ROOT as face_data_path
from PIL import Image
import imutils

from io import BytesIO
import base64

haar_file = 'haarcascade_frontalface_default.xml'
  
#Will save data here
def add_data(name):
    #Create a folder in your local drive and give the path below
    datasets =  face_data_path 
  
    sub_data = name     
  
    path = os.path.join(datasets, sub_data) 
    if not os.path.isdir(path): 
        os.mkdir(path) 
  
    # img sample size
    (width, height) = (130, 100)     
  
    face_cascade = cv2.CascadeClassifier(haar_file) 
    webcam = cv2.VideoCapture(0)  
  
    # Will caputure upto 30 img
    count = 1

    (_, im) = webcam.read() 
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 4) 
    for (x, y, w, h) in faces: 
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
        face = gray[y:y + h, x:x + w] 
        face_resize = cv2.resize(face, (width, height)) 
        cv2.imwrite('% s/% s.png' % (path), face_resize) 
        return face_resize
