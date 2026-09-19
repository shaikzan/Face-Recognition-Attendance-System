import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time



# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen,text_to_speech):
    if (l1 == "") and (l2==""):
        t='Please Enter the your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter the your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter the your Name.'
        text_to_speech(t)
    else:
        cam = None
        path = None
        try:
            Enrollment = l1.strip()
            Name = l2.strip()
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            if os.path.exists(path):
                message.configure(text="Student data already exists")
                text_to_speech("Student data already exists")
                return

            cam = cv2.VideoCapture(0)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not cam.isOpened():
                message.configure(text="Camera could not be opened")
                text_to_speech("Camera could not be opened")
                cam.release()
                cam = None
                return

            detector = cv2.CascadeClassifier(haarcasecade_path)
            sampleNum = 0
            cv2.namedWindow("Register Face", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Register Face", 800, 600)
            os.makedirs(path, exist_ok=False)
            while True:
                ret, img = cam.read()
                if not ret or img is None:
                    message.configure(text="Could not read from camera")
                    break
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(
                        os.path.join(
                            path,
                            Name + "_" + Enrollment + "_" + str(sampleNum) + ".jpg",
                        ),
                        gray[y : y + h, x : x + w],
                    )
                cv2.putText(
                    img,
                    f"Samples: {sampleNum}/50 - Press Q to stop",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )
                cv2.imshow("Register Face", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum >= 50:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [Enrollment, Name]
            with open(
                os.path.join(os.path.dirname(trainimage_path), "StudentDetails", "studentdetails.csv"),
                "a+",
            ) as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for ER No:" + Enrollment + " Name:" + Name
            message.configure(text=res)
            text_to_speech(res)
        except FileExistsError:
            message.configure(text="Student data already exists")
            text_to_speech("Student data already exists")
        except Exception:
            message.configure(text="Registration failed")
            text_to_speech("Registration failed")
        finally:
            if cam is not None:
                cam.release()
            try:
                cv2.destroyWindow("Register Face")
            except cv2.error:
                pass
