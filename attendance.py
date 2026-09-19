import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import threading
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# engine = pyttsx3.init()
# engine.say("Welcome!")
# engine.say("Please browse through your options..")
# engine.runAndWait()


speech_lock = threading.Lock()


def text_to_speech(user_text):
    def speak():
        with speech_lock:
            engine = pyttsx3.init()
            engine.say(user_text)
            engine.runAndWait()

    threading.Thread(target=speak, daemon=True).start()


base_dir = os.path.dirname(os.path.abspath(__file__))
haarcasecade_path = os.path.join(base_dir, "haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(base_dir, "TrainingImageLabel", "Trainner.yml")
trainimage_path = os.path.join(base_dir, "TrainingImage")
studentdetail_path = os.path.join(base_dir, "StudentDetails", "studentdetails.csv")
attendance_path = os.path.join(base_dir, "Attendance")
os.makedirs(trainimage_path, exist_ok=True)

window = Tk()
window.title("CLASS VISION")
window.geometry("1280x720")
window.minsize(1100, 650)
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="#1c1c1c")

# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x110")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)


def testVal(inStr, acttyp):
    if acttyp == "1":
        if not inStr.isdigit():
            return False
    return True


main_container = tk.Frame(window, bg="#1c1c1c")
main_container.pack(fill="both", expand=True, padx=24, pady=20)

header = tk.Frame(main_container, bg="#1c1c1c")
header.pack(fill="x", pady=(0, 10))

logo = Image.open(os.path.join(base_dir, "UI_Image", "0001.png"))
logo = logo.resize((50, 47), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
logo_label = tk.Label(header, image=logo1, bg="#1c1c1c")
logo_label.pack(side="left", padx=(0, 10))

titl = tk.Label(
    header,
    text="CLASS VISION",
    bg="#1c1c1c",
    fg="yellow",
    font=("Verdana", 27, "bold"),
)
titl.pack(side="left")

welcome = tk.Label(
    main_container,
    text="Welcome to CLASS VISION",
    bg="#1c1c1c",
    fg="yellow",
    bd=10,
    font=("Verdana", 30, "bold"),
)
welcome.pack(pady=(0, 30))

icon_row = tk.Frame(main_container, bg="#1c1c1c")
icon_row.pack(fill="x", pady=(0, 10))

ri = Image.open(os.path.join(base_dir, "UI_Image", "register.png"))
ri = ri.resize((120, 120), Image.LANCZOS)
r = ImageTk.PhotoImage(ri)
label1 = Label(icon_row, image=r, bg="#1c1c1c")
label1.image = r
label1.pack(side="left", expand=True)

vi = Image.open(os.path.join(base_dir, "UI_Image", "verifyy.png"))
vi = vi.resize((120, 120), Image.LANCZOS)
v = ImageTk.PhotoImage(vi)
label3 = Label(icon_row, image=v, bg="#1c1c1c")
label3.image = v
label3.pack(side="left", expand=True)

ai = Image.open(os.path.join(base_dir, "UI_Image", "attendance.png"))
ai = ai.resize((120, 120), Image.LANCZOS)
a = ImageTk.PhotoImage(ai)
label2 = Label(icon_row, image=a, bg="#1c1c1c")
label2.image = a
label2.pack(side="left", expand=True)

button_row = tk.Frame(main_container, bg="#1c1c1c")
button_row.pack(fill="x", pady=(10, 0))
button_row.grid_columnconfigure((0, 1, 2), weight=1)


def TakeImageUI():
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")  # Dark background for the image window
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#1c1c1c", fg="green", font=("Verdana", 30, "bold"),
    )
    titl.place(x=270, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",  # Dark background for the details label
        fg="yellow",  # Bright yellow text color
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(x=280, y=75)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",  # Dark background for messages
        fg="yellow",  # Bright text color for messages
        relief=RIDGE,
        font=("Verdana", 14, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="yellow",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="yellow",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)


register_btn = tk.Button(
    button_row,
    text="Register a new student",
    command=TakeImageUI,
    bd=8,
    font=("Verdana", 16),
    bg="#111111",
    fg="yellow",
    height=2,
    width=18,
    relief=RIDGE,
)
register_btn.grid(row=0, column=0, padx=18, pady=14, sticky="ew")


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


attendance_btn = tk.Button(
    button_row,
    text="Take Attendance",
    command=automatic_attedance,
    bd=8,
    font=("Verdana", 16),
    bg="#111111",
    fg="yellow",
    height=2,
    width=18,
    relief=RIDGE,
)
attendance_btn.grid(row=0, column=1, padx=18, pady=14, sticky="ew")


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


view_btn = tk.Button(
    button_row,
    text="View Attendance",
    command=view_attendance,
    bd=8,
    font=("Verdana", 16),
    bg="#111111",
    fg="yellow",
    height=2,
    width=18,
    relief=RIDGE,
)
view_btn.grid(row=0, column=2, padx=18, pady=14, sticky="ew")

exit_btn = tk.Button(
    main_container,
    text="EXIT",
    bd=8,
    command=quit,
    font=("Verdana", 16),
    bg="#111111",
    fg="yellow",
    height=2,
    width=18,
    relief=RIDGE,
)
exit_btn.pack(pady=(10, 0))


window.mainloop()
