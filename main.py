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

# Load questions dataset
try:
    questions = pd.read_csv('questions.csv')
except FileNotFoundError:
    print("Error: 'questions.csv' not found.")
    exit()

wrong_answer=[]

# Initialize hand detector
detector = HandDetector()

# Initialize variables
score = 0
current_question = 0
total_questions = len(questions)
question_start_time = time.time()
answer_check_interval = 5  # Interval for answer checking
last_answer_check = time.time()

# Setup video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height
ptime = 0  # For FPS calculation

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    img = detector.findHands(img)
    beforeAns_time = time.time() - question_start_time

    # Display question and options
    question = questions['Question'][current_question]
    option1 = questions['Option 1'][current_question]
    option2 = questions['Option 2'][current_question]
    option3 = questions['Option 3'][current_question]
    option4 = questions['Option 4'][current_question]
    correct_option = questions['Correct Option'][current_question]

    cv2.putText(img, f"Score: {score}", (1000, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"Q: {question}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"1: {option1}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(img, f"2: {option2}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(img, f"3: {option3}", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(img, f"4: {option4}", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Show "Answer now" prompt after 20 seconds
    if beforeAns_time > 10:
        cv2.putText(img, "Answer now", (500, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Check for hand gesture every 5 seconds
        if time.time() - last_answer_check > answer_check_interval:
            position = detector.findPosition(img)
            if position:
                finger_count = counting(position)
                print(f"Number of fingers detected: {finger_count}")

                if 1 <= finger_count <= 4:
                    selected_option = questions[f'Option {finger_count}'][current_question]
                    if selected_option == correct_option:
                        cv2.putText(img, "Correct!", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        score += 1
                    else:
                        cv2.putText(img, "Wrong!", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        wrong_answer.append(current_question)
                        print(wrong_answer)

                    # Move to next question
                    current_question += 1
                    if current_question >= total_questions:
                        break

                    # Reset timers for next question
                    question_start_time = time.time()
                    last_answer_check = question_start_time
            else:
                print("No hands detected.")
            last_answer_check = time.time()

    # Automatically skip to the next question after 30 seconds
    if beforeAns_time > 30:
        print("Time's up for this question.")
        current_question += 1
        if current_question >= total_questions:
            break
        question_start_time = time.time()
        last_answer_check = question_start_time

    # Calculate and display FPS
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 700), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Quiz", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"Final Score: {score}/{total_questions}")
with open("score.txt", "w") as file:
    file.write(f"{score} /{total_questions}\n{wrong_answer}")

import final