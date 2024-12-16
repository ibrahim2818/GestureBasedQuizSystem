import mediapipe as mp
import cv2
import time

class FaceDetector:
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw=True):
        # Convert the image to RGB
        face_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.faceDetection.process(face_image)

        face_count = 0  # Initialize face count
        if self.result.detections:
            face_count = len(self.result.detections)  # Count the number of faces
            for id, detection in enumerate(self.result.detections):
                if draw:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = img.shape
                    bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                           int(bboxC.width * iw), int(bboxC.height * ih)
                    cv2.rectangle(img, bbox, (255, 0, 255), 2)

        return img, face_count  # Return the processed image and face count

    def faceCount(self, img):
        # Convert the image to RGB
        face_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.faceDetection.process(face_image)

        # Return the number of detections
        if self.result.detections:
            return len(self.result.detections)
        return 0  # If no detections, return 0


def main():
    ptime = 0

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = FaceDetector(minDetectionCon=0.75)

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Process the image and get face count
        img, face_count = detector.findFaces(img)  # Process the image to find faces
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        # Display the FPS and face count
        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 255), 3)
        cv2.putText(img, f"Faces: {face_count}", (10, 130), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 3)

        cv2.imshow("Image", img)

        # Print face count to the console
        print(f"Faces detected: {face_count}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
