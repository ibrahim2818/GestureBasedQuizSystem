import pandas as pd
import cv2
from HandTracking import HandDetector
import time
#importing the data set
data = pd.read_csv('questions.csv')

#creating the object
detector =HandDetector()
ptime = 0
ctime = 0

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    img = detector.findHands(img)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 255), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()