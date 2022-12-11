import cv2
from pyclass.Recognition.Video import Video
from pyclass.Recognition.VideoFlags import VideoFlags as vf

if __name__ == '__main__':
    video = Video(0, flags=vf.VIDEOFACE)

    while cv2.waitKey(30) & 0xff != 27:
        image, data = video.fetchData()
        cv2.imshow('img', image)
        print(data)

    video.release()
