import cv2
import numpy as np
from os import listdir
from os.path import isfile, join


class BodyDetector(cv2.HOGDescriptor):
    def __init__(self, pathVideo=0, pathXML="data/body_xml/"):
        super().__init__()
        self.screen = cv2.VideoCapture(pathVideo)
        self.xmls = [pathXML + file for file in listdir(pathXML) if isfile(join(pathXML, file))]

    def updateData(self, draw=True):
        # Retrieve the image data till success
        success, image = self.screen.read()
        if not success:
            raise Exception(f"Fetching image data is not succeed.")
        body = None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Retrieve all faces analysing by xml shapes
        for xml in self.xmls:
            pass

        # Draw all detected faces
        if draw:
            for (x, y, w, h) in body:
                if all([x, y, w, h]):
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return (image, body)
