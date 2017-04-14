#!/usr/bin/env python
import cv2

class HaarDetector:

    def __init__(self, cascade_path):
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def detect(self, image_path, min_size, max_object_count):
        raw_image = cv2.imread(image_path)
        grayscale_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)

        objects = self.cascade.detectMultiScale(grayscale_image, scaleFactor = 1.2,
                                             minNeighbors = 5, minSize = min_size,
                                             flags = cv2.CASCADE_SCALE_IMAGE)
        object_count = len(objects)
        return object_count > 0 and object_count <= max_object_count
