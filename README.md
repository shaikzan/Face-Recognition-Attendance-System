# Face Recognition Attendance System

A face-recognition-based attendance management system that automates student identification and attendance recording using computer vision and machine learning.

The project contains **two implementations**:

* **Desktop Application** — Python, OpenCV, Tkinter, Haar Cascade, LBPH, Pandas, and CSV storage.
* **Web Application** — Next.js, React, TypeScript, Flask, MongoDB, MTCNN, DeepFace, and FaceNet512.

The system allows students to register their details and face images, trains or generates facial representations, recognizes students through a webcam, and records their attendance automatically.

## Key Features

* Student registration
* Webcam-based face capture
* Real-time face detection and recognition
* Automated attendance marking
* Duplicate attendance prevention
* Subject-wise attendance records
* Attendance percentage calculation
* Desktop GUI
* Web-based dashboard
* MongoDB-based student and face-embedding storage
* CSV-based attendance storage for the desktop version
* Browser camera integration
* Voice feedback in the desktop application

## Technology Stack

**Desktop**

* Python
* OpenCV
* Haar Cascade
* LBPH Face Recognizer
* Tkinter
* Pandas
* Pillow
* CSV
* pyttsx3

**Web**

* Next.js
* React
* TypeScript
* Tailwind CSS
* Flask
* MongoDB
* DeepFace
* FaceNet512
* MTCNN
* Bcrypt

## System Workflow

```text
Student Registration
        ↓
Capture Face Images
        ↓
Face Detection
        ↓
Training / Face Embedding Generation
        ↓
Webcam Recognition
        ↓
Student Identification
        ↓
Attendance Recording
        ↓
Attendance Reports
```

The desktop implementation uses **Haar Cascade + LBPH**, while the web implementation uses **MTCNN + FaceNet512 through DeepFace**.

This project demonstrates the integration of computer vision, machine learning, web development, databases, and automated attendance management in a single system.
