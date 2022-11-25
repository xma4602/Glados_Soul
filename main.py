import cv2
from cvzone.PoseModule import PoseDetector
from cvzone.FaceDetectionModule import FaceDetector

if __name__ == '__main__':

    # Initialization
    cap = cv2.VideoCapture(0)
    poseDetector = PoseDetector()
    faceDetector = FaceDetector()

    while True:
        # Retrieve the image data till success
        success, img = cap.read()
        if not success:
            continue

        # Find poses & faces
        img = poseDetector.findPose(img)
        img, bboxs = faceDetector.findFaces(img)

        # Draw detected faces
        if bboxs:
            # bboxInfo - "id","bbox","score","center"
            center = bboxs[0]["center"]
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        # Draw detected poses & body particles
        lmList, bboxInfo = poseDetector.findPosition(img, bboxWithHands=False)
        if bboxInfo:
            center = bboxInfo["center"]
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

        # Show the result
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fin
    cap.release()
    cv2.destroyAllWindows()
