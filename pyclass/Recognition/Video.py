import cv2
import numpy as np

from pyclass.Recognition.FaceDetector import FaceDetector
from pyclass.Recognition.BodyDetector import BodyDetector
from pyclass.Recognition.VideoFlags import VideoFlags as vf


class Video(cv2.VideoCapture):

    def __init__(self, pathVideo, flags=vf.VIDEOFACE | vf.VIDEOBODY):
        super().__init__(pathVideo)
        self.bodyDetector = BodyDetector(self)
        self.faceDetector = FaceDetector(self)
        self.flags = flags
        self.image = None

    def fetchData(self, draw=True):
        global VIDEOFACE, VIDEOBODY
        # Retrieve the image data till success
        success, self.image = self.read()
        if not success:
            raise Exception(f"Fetching image data is not succeed.")

        data = dict()

        if self.flags >= vf.VIDEOFACE:
            data["faces"] = self.faceDetector.updateData()
        if self.flags >= vf.VIDEOBODY:
            data["body"] = self.bodyDetector.updateData()

        # Draw all detected items
        if draw:
            for key in data.keys():
                if data[f'{key}'] is None:
                    continue
                for (x, y, w, h) in data[f'{key}']:
                    if all([x, y, w, h]):

                        cv2.rectangle(self.image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return (self.image, data)
