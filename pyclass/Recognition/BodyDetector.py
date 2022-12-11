import cv2
import numpy as np
from os import listdir
from os.path import isfile, join


class BodyDetector(cv2.HOGDescriptor):
    def __init__(self, screen, pathXML="data/body_xml/"):
        super().__init__()
        self.screen = screen
        self.xmls = [pathXML + file for file in listdir(pathXML) if isfile(join(pathXML, file))]

    def updateData(self):
        body = None
        gray = cv2.cvtColor(self.screen.image, cv2.COLOR_BGR2GRAY)

        # Retrieve all faces analysing by xml shapes
        for xml in self.xmls:
            pass

        return body
