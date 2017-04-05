#!/usr/bin/env python
import cv2

class Cv2HumanDetector:

    def __init__(self):
        self.cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")

    def is_potentially_human(self, image_path, max_human_count):
        raw_image = cv2.imread(image_path)
        grayscale_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

        faces = self.cascade.detectMultiScale(grayscale_image, scaleFactor = 1.1,
                                             minNeighbors = 5, minSize=(30, 30),
                                             flags = cv2.CASCADE_SCALE_IMAGE)
        face_count = len(faces)
        return face_count > 0 and face_count <= max_human_count
