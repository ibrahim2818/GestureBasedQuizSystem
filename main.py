import pandas as pd
import cv2
from HandTracking import HandDetector
import time

def counting(x):
    count = 0
    if x[6][2] > x[8][2]:
        count += 1
    if x[12][2] < x[10][2]:
        count += 1
    if x[16][2] < x[14][2]:
        count += 1
    if x[20][2] < x[18][2]:
        count += 1
    if x[4][1] < x[2][1]:
        count += 1
    return count

# Initialize variables
last_time = time.time()
score = 0

# Load questions dataset
questions = pd.read_csv('questions.csv')

# Initialize hand detector
detector = HandDetector()
ptime = 0
ctime = 0

current_question = 0
total_questions = len(questions)

# Setup video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    img = detector.findHands(img)
    finger = 0

    if time.time() - last_time > 5:
        position = detector.findPosition(img)
        if position:
            finger = counting(position)
            print(f"Number of fingers: {finger}")
        else:
            print("No hands detected")
        last_time = time.time()

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    # Display current question and options
    question = questions['Question'][current_question]
    option1 = questions['Option 1'][current_question]
    option2 = questions['Option 2'][current_question]
    option3 = questions['Option 3'][current_question]
    option4 = questions['Option 4'][current_question]
    answer = questions['Correct Option'][current_question]

    cv2.putText(img, f"Score: {score}", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"FPS: {int(fps)}", (10, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.putText(img, f"Q: {question}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"1: {option1}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(img, f"2: {option2}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(img, f"3: {option3}", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(img, f"4: {option4}", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    if finger > 0 and finger < 5:
        if finger == 1:
            if answer == option1:
                cv2.putText(img, "Correct", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                score += 1
            else:
                print("Wrong")
            current_question += 1
        elif finger == 2:
            if answer == option2:
                cv2.putText(img, "Correct", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                score += 1
            else:
                print("Wrong")
            current_question += 1
        elif finger == 3:
            if answer == option3:
                cv2.putText(img, "Correct", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                score += 1
            else:
                print("Wrong")
            current_question += 1
        elif finger == 4:
            if answer == option4:
                cv2.putText(img, "Correct", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                score += 1
            else:
                print("Wrong")
            current_question += 1

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q') or current_question >= total_questions:
        print("Score:", score)
        break

cap.release()
cv2.destroyAllWindows()
