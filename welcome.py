from tkinter import *
from PIL import Image, ImageTk

def start_quiz():
    welcome.destroy()
    import main


welcome = Tk()
welcome.title("Welcome")
welcome.geometry("1280x720")

# Open the image using PIL and convert it to a format Tkinter can work with
img = Image.open("C:\\Users\\mdabr\\PycharmProjects\\GestureBasedQuizSystem\\Welcome.jpg")
#img = img.resize((1280, 720), Image.ANTIALIAS)  # Resize if needed
img_tk = ImageTk.PhotoImage(img)

label = Label(welcome, image=img_tk)
label.place(x=0, y=0)


startButton = Button(welcome, text="Start Quiz",font=("Open Sans Bold", 30, "bold"),
                     command=start_quiz, bg="white", fg="black",border=0)
startButton.place(x=470, y=380)

# Keep a reference to the image to avoid garbage collection
label.image = img_tk

welcome.mainloop()
