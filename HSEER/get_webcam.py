import cv2
from facenet_pytorch import MTCNN
import torch
from . import HSEER_model
import os
from flask import flash

DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
SNAPS_DIR = 'HSEER/snaps/'


class WebCam:
    def __init__(self):
        self.face_recognizer = MTCNN(keep_all=False, post_process=False, min_face_size=40, device=DEVICE)

    def detect_face(self):
        webcam = cv2.VideoCapture(0)
        while True:
            success, frame = webcam.read()
            if not success:
                print('!failed to grab a frame')

            img_name = SNAPS_DIR + 'user_photo.jpg'
            if not cv2.imwrite(img_name, frame):
                raise Exception('couldn\'t write an image')
            else:
                break
        
        webcam.release()
        face_image = HSEER_model.detect_face(img_name, self.face_recognizer)
        os.remove(img_name)
        if isinstance(face_image, bool):
            flash('Failed to detect face!', category='error')
        else:
            return face_image
        