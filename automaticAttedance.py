import tkinter as tk
import tkinter
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
import tkinter.ttk as tkk
import tkinter.font as font

base_dir = os.path.dirname(os.path.abspath(__file__))
haarcasecade_path = os.path.join(base_dir, "haarcascade_frontalface_default.xml")
trainimagelabel_path = os.path.join(base_dir, "TrainingImageLabel", "Trainner.yml")
trainimage_path = os.path.join(base_dir, "TrainingImage")
studentdetail_path = os.path.join(base_dir, "StudentDetails", "studentdetails.csv")
attendance_path = os.path.join(base_dir, "Attendance")
# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    subject = tk.Toplevel()
    subject.title("Class Vision | Take Attendance")
    subject.geometry("1180x720")
    subject.minsize(1000, 650)
    subject.configure(background="#111827")

    colors = {
        "background": "#111827",
        "panel": "#1f2937",
        "panel_dark": "#0f172a",
        "preview": "#0f172a",
        "border": "#374151",
        "text": "#f9fafb",
        "muted": "#9ca3af",
        "accent": "#38bdf8",
        "success": "#34d399",
    }

    header = tk.Frame(subject, bg=colors["background"])
    header.pack(fill="x", padx=28, pady=(24, 16))
    tk.Label(
        header,
        text="TAKE ATTENDANCE",
        bg=colors["background"],
        fg=colors["text"],
        font=("Segoe UI", 24, "bold"),
    ).pack(anchor="w")
    tk.Label(
        header,
        text="Start recognition, verify students, and save today's attendance.",
        bg=colors["background"],
        fg=colors["muted"],
        font=("Segoe UI", 11),
    ).pack(anchor="w", pady=(4, 0))

    Notifica = tk.Label(
        subject,
        text="Ready for a subject",
        bg=colors["panel"],
        fg=colors["success"],
        anchor="w",
        padx=18,
        font=("Segoe UI", 11, "bold"),
    )
    Notifica.place(x=28, y=650, width=1124, height=42)

    def ui_status(message_text, fg="yellow", bg="black"):
        try:
            if bg == "black":
                bg = colors["panel"]
            if fg == "yellow":
                fg = colors["text"]
            Notifica.configure(text=message_text, bg=bg, fg=fg, width=40, height=2)
            Notifica.place(x=28, y=650, width=1124, height=42)
            subject.update_idletasks()
        except Exception:
            pass

    def reset_capture_button():
        try:
            fill_a.configure(state="normal")
        except NameError:
            pass

    def show_result(file_name):
        root = tk.Toplevel(subject)
        root.title("Attendance of " + tx.get().strip())
        root.configure(background="black")
        with open(file_name, newline="") as f:
            reader = csv.reader(f)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1

    alert_label = tk.Label(
        subject,
        bg=colors["preview"],
        fg=colors["accent"],
        text="LIVE CAMERA PREVIEW",
        font=("Segoe UI", 11, "bold"),
    )
    alert_label.place(x=28, y=105, width=700, height=34, anchor="nw")
    preview_label = tk.Label(
        subject,
        bg=colors["preview"],
        text="Enter a subject, then click\nStart Recognition",
        fg=colors["muted"],
        width=70,
        height=25,
        font=("Segoe UI", 13),
    )
    preview_label.place(x=28, y=139, width=700, height=490)

    def finish_attendance(cam, attendance, sub, start_time):
        if attendance.empty:
            ui_status("No valid face was detected. Attendance not saved.", fg="yellow", bg="black")
            text_to_speech("No valid face was detected. Attendance not saved.")
            if cam is not None:
                cam.release()
            cv2.destroyAllWindows()
            reset_capture_button()
            return

        ts = time.time()
        today = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        Hour, Minute, Second = timeStamp.split(":")
        path = os.path.join(attendance_path, sub)
        os.makedirs(path, exist_ok=True)
        file_name = os.path.join(
            path,
            sub + "_" + today + "_" + Hour + "-" + Minute + "-" + Second + ".csv",
        )
        attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
        attendance[today] = 1
        attendance.to_csv(file_name, index=False)

        msg = "Attendance saved for " + sub + "."
        ui_status(msg, fg="yellow", bg="black")
        text_to_speech(msg)

        if cam is not None:
            cam.release()
        cv2.destroyAllWindows()
        show_result(file_name)

    def process_attendance():
        sub = tx.get().strip()
        if sub == "":
            ui_status("Please enter the subject name!!!", fg="yellow", bg="black")
            text_to_speech("Please enter the subject name!!!")
            reset_capture_button()
            return

        try:
            ui_status("Checking model and camera...", fg="yellow", bg="black")
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except Exception:
                e = "Model not found,please train model"
                ui_status(e, fg="yellow", bg="black")
                text_to_speech(e)
                reset_capture_button()
                return

            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)
            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not cam.isOpened():
                e = "Camera could not be opened"
                ui_status(e, fg="yellow", bg="black")
                text_to_speech(e)
                reset_capture_button()
                return

            ui_status("Attendance is running... stay in front of the camera", fg="yellow", bg="black")
            attendance = pd.DataFrame(columns=["Enrollment", "Name"])
            start_time = time.time()
            deadline = start_time + 20

            frame_number = 0

            def update_frame():
                nonlocal frame_number
                nonlocal attendance
                if time.time() > deadline:
                    finish_attendance(cam, attendance, sub, start_time)
                    return

                ret, frame = cam.read()
                if not ret or frame is None:
                    ui_status("Camera stream lost. Please try again.", fg="yellow", bg="black")
                    cam.release()
                    reset_capture_button()
                    return

                frame_number += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = []
                if frame_number % 2 == 0:
                    faces = facecasCade.detectMultiScale(
                        gray,
                        scaleFactor=1.2,
                        minNeighbors=5,
                        minSize=(60, 60),
                    )
                for (x, y, w, h) in faces:
                    face = gray[y : y + h, x : x + w]
                    Id, conf = recognizer.predict(face)
                    if conf < 70:
                        aa = df.loc[df["Enrollment"] == Id]["Name"].values
                        if len(aa) == 0:
                            continue
                        name = str(aa[0])
                        if not ((attendance["Enrollment"].astype(str) == str(Id)) & (attendance["Name"].astype(str) == name)).any():
                            attendance.loc[len(attendance)] = [Id, name]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 260, 0), 4)
                        cv2.putText(frame, f"{Id}-{name}", (x + h, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 4)
                        ui_status(f"Detected: {Id} - {name}", fg="yellow", bg="black")
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(frame, "Unknown", (x + h, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 25, 255), 4)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                image = image.resize((640, 480), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                preview_label.configure(image=photo, text="")
                preview_label.image = photo
                subject.update_idletasks()
                subject.after(80, update_frame)

            update_frame()

        except Exception as error:
            ui_status(f"Attendance error: {error}", fg="white", bg="#8b0000")
            text_to_speech("Attendance could not be completed")
            reset_capture_button()
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass

    def FillAttendance():
        fill_a.configure(state="disabled")
        ui_status("Opening attendance screen...", fg="yellow", bg="black")
        subject.after(50, process_attendance)

    def Attf():
        sub = tx.get().strip()
        if sub == "":
            ui_status("Enter a subject name before opening sheets.", fg="yellow", bg="black")
            text_to_speech("Please enter the subject name!!!")
            return

        subject_dir = os.path.join(attendance_path, sub)
        if not os.path.isdir(subject_dir):
            ui_status(f"No attendance sheets found for '{sub}'.", fg="yellow", bg="black")
            text_to_speech("No attendance sheets found for this subject.")
            return

        os.startfile(subject_dir)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=0,
        font=("Segoe UI", 11, "bold"),
        bg=colors["panel_dark"],
        fg=colors["text"],
        activebackground="#1e293b",
        activeforeground=colors["text"],
        height=2,
        width=18,
        relief=tk.FLAT,
    )
    attf.place(x=770, y=355, width=330, height=52)

    sub = tk.Label(
        subject,
        text="SUBJECT NAME",
        bg=colors["panel"],
        fg=colors["text"],
        font=("Segoe UI", 11, "bold"),
    )
    sub.place(x=770, y=139, width=330, height=32, anchor="nw")

    tx = tk.Entry(
        subject,
        width=15,
        bd=0,
        bg=colors["preview"],
        fg=colors["text"],
        insertbackground=colors["text"],
        relief=tk.FLAT,
        font=("Segoe UI", 18),
    )
    tx.place(x=770, y=178, width=330, height=52)

    fill_a = tk.Button(
        subject,
        text="START RECOGNITION",
        command=FillAttendance,
        bd=0,
        font=("Segoe UI", 11, "bold"),
        bg=colors["accent"],
        fg="#082f49",
        activebackground="#7dd3fc",
        activeforeground="#082f49",
        height=2,
        width=18,
        relief=tk.FLAT,
    )
    fill_a.place(x=770, y=245, width=330, height=58)

    tk.Label(
        subject,
        text="The camera will run for 20 seconds and save\nrecognized students to the subject folder.",
        bg=colors["panel"],
        fg=colors["muted"],
        justify="left",
        font=("Segoe UI", 10),
    ).place(x=770, y=430, width=330, height=48, anchor="nw")
