import cv2
import numpy as np
from os import listdir
from os.path import isfile, join


class FaceDetector(cv2.CascadeClassifier):
    def __init__(self, screen, pathXML="data/faces_xml/"):
        super().__init__()
        self.screen = screen
        self.xmls = [pathXML + file for file in listdir(pathXML) if isfile(join(pathXML, file))]

    def updateData(self):
        faces = None
        gray = cv2.cvtColor(self.screen.image, cv2.COLOR_BGR2GRAY)

        # Retrieve all faces analysing by xml shapes
        for xml in self.xmls:
            self.load(xml)
            data = self.detectMultiScale(
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

        return faces
