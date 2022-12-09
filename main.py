import cv2
from pyclass.Recognition.FaceDetector import FaceDetector
from pyclass.Recognition.BodyDetector import BodyDetector
import time

if __name__ == '__main__':
    faceDetector = FaceDetector()
    bodyDetector = BodyDetector()
    while cv2.waitKey(30) & 0xff != 27:
        image, faces = faceDetector.updateData()
        cv2.imshow('img', image)
        print(faces)

    faceDetector.screen.release()
