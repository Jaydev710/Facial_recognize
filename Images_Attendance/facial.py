import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import serial
import time
import pyttsx3  # Text-to-Speech library

# Initialize the Text-to-Speech engine
tts_engine = pyttsx3.init()

def text_to_speech(name):
    """Convert text to speech."""
    try:
        tts_engine.say(f"FACE DETECTED, {name}")
        time.sleep(4)
        tts_engine.runAndWait()
        print(f"[INFO] Text-to-Speech: Hello, {name}")
    except Exception as e:
        print(f"[ERROR] Text-to-Speech failed: {e}")

# Serial communication setup
def setup_serial():
    MAX_RETRIES = 10
    retries = 0
    port = None

    while not port and retries < MAX_RETRIES:
        try:
            port = serial.Serial("COM11", 115200, timeout=1)
            print("[INFO] Connected to ESP32 on COM11.")
        except serial.SerialException as e:
            retries += 1
            print(f"[WARNING] Attempt {retries}/{MAX_RETRIES}: Unable to connect to ESP32. Retrying...")
            time.sleep(2)

    if not port:
        raise Exception("[ERROR] Could not connect to ESP32 after multiple attempts. Check connections and COM port.")
    
    return port

# Serial port initialization
try:
    serial_port = setup_serial()
    print("[INFO] Serial communication established.")
except Exception as e:
    print(e)
    exit()

def send_to_esp32(command):
    """Send commands to ESP32."""
    try:
        serial_port.write((command + '\n').encode())
        print(f"[INFO] Sent command '{command}' to ESP32.")
    except Exception as e:
        print(f"[ERROR] Could not send command to ESP32: {e}")

def handle_face_recognition(recognized):
    """Send appropriate command based on face recognition result."""
    if recognized:
        send_to_esp32("1")
    else:
        send_to_esp32("0")

def findEncodings(images):
    """Encode known images."""
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        if encode:
            encodeList.append(encode[0])
        else:
            print(f"[WARNING] Encoding failed for an image.")
    return encodeList

def markAttendance(name):
    """Mark attendance for recognized name."""
    file_path = 'Attendance.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("Name,Time,Date\n")
    with open(file_path, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M:%S')
            dString = time_now.strftime('%d/%m/%Y')
            f.writelines(f'{name},{tString},{dString}\n')
            print(f"[INFO] Marked attendance for {name}.")

# Path to the directory containing images
path = r"C:\Users\JAYDEV RAJAIYA\Desktop\q\Images_Attendance"

if not os.path.exists(path):
    print(f"[ERROR] Directory '{path}' does not exist!")
    os.makedirs(path)
    print(f"[INFO] Created missing directory '{path}'.")

images = []
classNames = []

myList = os.listdir(path)
print("[INFO] Images found in directory:", myList)

for cl in myList:
    if cl.endswith(('.png', '.jpg', '.jpeg')):
        curImg = cv2.imread(os.path.join(path, cl))
        if curImg is not None:
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        else:
            print(f"[WARNING] Could not read file '{cl}' as an image.")
    else:
        print(f"[INFO] Skipping non-image file '{cl}'.")

print("[INFO] Class names:", classNames)

encodeListKnown = findEncodings(images)
print('[INFO] Encoding Complete.')

# Start webcam for real-time face recognition
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("[ERROR] Failed to read from webcam.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    recognized = False
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            markAttendance(name)
            text_to_speech(name)  # Speak the recognized name
            handle_face_recognition(recognized=True)
            recognized = True

    if not recognized:
        handle_face_recognition(recognized=False)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(10) == 13:  # Press 'Enter' key to exit
        break

cap.release()
cv2.destroyAllWindows()
