import cv2
import mediapipe as mp
#import time




class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = float(detectionCon)
        self.trackCon = float(trackCon)
        self.frame_count=0
        self.for_skip_frame=3
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils





    def findHands(self, img, draw=True):
        if self.frame_count % self.for_skip_frame==0:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(imgRGB)
        self.frame_count +=1

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mphands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return lmList

# def main():
#     ptime = 0
#     ctime = 0
#
#     cap = cv2.VideoCapture(0)
#     cap.set(3, 1280)
#     cap.set(4, 720)
#     detector = HandDetector()
#
#     while cap.isOpened():
#         success, img = cap.read()
#         if not success:
#             print("Ignoring empty camera frame.")
#             continue
#
#         img = detector.findHands(img)
#         ctime = time.time()
#         fps = 1 / (ctime - ptime)
#         ptime = ctime
#         cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN,
#                     3, (255, 0, 255), 3)
#
#         cv2.imshow("Image", img)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
# if __name__ == "__main__":
#     main()
