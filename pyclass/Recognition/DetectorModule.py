import cv2
import numpy as np
from os import listdir
from os.path import isfile, join


class FaceDetector:
    def __init__(self, screen, pathXML="data/faces_xml/"):
        self.faceCascade = cv2.CascadeClassifier()
        self.screen = screen
        self.xmls = [pathXML + file for file in listdir(pathXML) if isfile(join(pathXML, file))]

    def updateData(self, draw=True):
        # Retrieve the image data till success
        success, image = self.screen.read()
        if not success:
            raise Exception(f"Fetching image data is not succeed.")
        faces = None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Retrieve all faces analysing by xml shapes
        for xml in self.xmls:
            self.faceCascade.load(xml)
            data = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=4,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if (faces is None):
                faces = data
            elif (data is np.ndarray):
                faces = np.concatenate((faces, data), axis=0)

        # Draws all detected faces
        if draw:
            for (x, y, w, h) in faces:
                if all([x, y, w, h]):
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return (image, faces)
