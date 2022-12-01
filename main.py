import cv2
from pyclass.Recognition.DetectorModule import FaceDetector


if __name__ == '__main__':
    screen = cv2.VideoCapture(0)
    faceDetector = FaceDetector(screen)
    k = 0
    while k != 27:
        image, faces = faceDetector.updateData()
        cv2.imshow('img', image)
        k = cv2.waitKey(30) & 0xff

        print(faces)

    faceDetector.screen.release()
