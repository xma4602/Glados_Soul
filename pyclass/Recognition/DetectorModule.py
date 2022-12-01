import cv2
import numpy as np


class FaceDetector:
    def __init__(self, screen):
        self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        self.screen = screen
        self.image = None
        self.faces = None

    def updateData(self):
        # Retrieve the image data till success
        success, self.image = self.screen.read()

        if not success:
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.faces = self.faceCascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return (self.image, self.faces)

