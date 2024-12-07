from tkinter import *
from PIL import ImageTk, Image
import ast
import pandas as pd

qsdata= pd.read_csv("questions.csv")

#from main import wrong_answer

finalWindow = Tk()
finalWindow.title("Score")
finalWindow.geometry("1280x720")

img= Image.open("scorepage.png")
img_tk = ImageTk.PhotoImage(img)

label = Label(finalWindow, image=img_tk)
label.place(x=0, y=0)

with open("score.txt") as file:
    data= file.readlines()

line1= data[0].strip()
wrong_answers =ast.literal_eval(data[1].strip())
wrong_answers= [int(i) for i in wrong_answers]

print(wrong_answers)

scoreLabel= Label(finalWindow, text=f"Your Score: {line1}", font=("Open Sans Bold", 30, "bold"),bg="white", fg="black")
scoreLabel.place(x=50, y=120)
for i in range(len(wrong_answers)):
    wrong_answerLabel= Label(finalWindow, text=f"Question {i+1} : {qsdata['Question'][wrong_answers[i]]} \nRight Answer: {qsdata['Correct Option'][wrong_answers[i]]}",
                             font=("Open Sans Bold", 10, "bold",),justify="left",bg="white", fg="black")
    wrong_answerLabel.place(x=50, y=200+i*50)


if ((len(qsdata)-len(wrong_answers))/len(qsdata))*100>80:
    motivationLabel= Label(finalWindow, text="Outstanding work! Keep aiming for the stars, and you’ll continue to shine brighter every day.",
                           font=("Open Sans Bold", 18, "bold"),bg="white", fg="black")
    motivationLabel.place(x=30, y=650)
elif ((len(qsdata)-len(wrong_answers))/len(qsdata))*100>50:
    motivationLabel= Label(finalWindow, text="Great job! You’re doing fantastic, and just a little more effort can take you to the top.",
                           font=("Open Sans Bold", 18, "bold"),bg="white", fg="black")
    motivationLabel.place(x=30, y=650)
else:
    motivationLabel= Label(finalWindow, text="Failure is not the opposite of success; it’s part of the journey. Keep trying—you’ll get there!",
                           font=("Open Sans Bold", 18, "bold"),bg="white", fg="black")
    motivationLabel.place(x=30, y=650)






finalWindow.mainloop()