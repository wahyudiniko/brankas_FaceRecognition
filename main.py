#test lcd
from rpi_lcd import LCD
from mail import sendEmail
import RPi.GPIO as GPIO
import face_recognition
import cv2
import numpy as np
import os
import time


buzzer = 4
ledRed = 23
ledGreen = 24
relay = 18
countT = 0
countD = 0
countSalah = 0

# GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)

# keypad matrix
MATRIX = [ [1, 2, 3, "A"],
           [4, 5, 6, "B"],
           [7, 8, 9, "C"],
           ["*", 0, "#", "D"] ]

ROW = [5, 6, 13, 19]
COL = [16, 20, 21, 12]

password = "1810D"
passEnter = ""
passStars = ""

# Note: This script requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# Visit smartbuids.io for more information

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# LCD object
lcd = LCD()

# Store objects in array
known_person=[] # Name of person string
known_image=[] # Image object
known_face_encodings=[] # Encoding object

# Initialize some lists
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def kirimWajah():
    cv2.imwrite('src/saved_image/img.jpg', frame)
    sendEmail('src/saved_image/img.jpg')

def benar():
    time.sleep(0.1)
    lcd.text("BRANKAS TERBUKA", 1)
    lcd.text("", 2)
    print("BRANKAS TERBUKA")
    GPIO.output(relay, 0)
    GPIO.output(ledGreen, 1)
    GPIO.output(ledRed, 0)

    GPIO.output(buzzer, 1)
    time.sleep(0.1)
    GPIO.output(buzzer, 0)
    time.sleep(0.1)
    GPIO.output(buzzer, 1)
    time.sleep(0.3)
    GPIO.output(buzzer, 0)

    time.sleep(1)
    lcd.text("'D' UNTUK KUNCI ", 2)


def pinSalah():   ################
    lcd.text("    PIN YANG", 1)
    lcd.text("DIMASUKKAN SALAH", 2)
    print("PIN SALAH")
    GPIO.output(relay, 1)
    GPIO.output(ledGreen, 0)
    GPIO.output(ledRed, 1)

    GPIO.output(buzzer, 1)
    time.sleep(1)
    GPIO.output(buzzer, 0)

def tDikenal():   ################
    lcd.text("  WAJAH TIDAK", 1)
    lcd.text("     SESUAI   ", 2)
    print("WAJAH TIDAK DIKENAL")
    GPIO.output(relay, 1)
    GPIO.output(ledGreen, 0)
    GPIO.output(ledRed, 1)

    GPIO.output(buzzer, 1)
    time.sleep(1)
    GPIO.output(buzzer, 0)

def noWajah():   ################
    time.sleep(0.1)
    lcd.text("  WAJAH TIDAK", 1)
    lcd.text("   TERDETEKSI   ", 2)
    print("WAJAH TAK TERDETEKSI")
    GPIO.output(relay, 1)
    GPIO.output(ledGreen, 0)
    GPIO.output(ledRed, 1)

    GPIO.output(buzzer, 1)
    time.sleep(1)
    GPIO.output(buzzer, 0)


lcd.text("initializing...", 1)
GPIO.output(ledGreen, 1)
GPIO.output(ledRed, 1)
GPIO.output(buzzer, 0)
GPIO.output(relay, 1))

#Loop to add images in friends folder
for file in os.listdir("src/profiles"):
    try:
        #Extracting person name from the image filename eg: david.jpg
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("src/profiles/", file)
        known_image = face_recognition.load_image_file(file)
        known_face_encodings.append(face_recognition.face_encodings(known_image)[0])

    except Exception as e:
        pass

# KEYPAD
for j in range(4):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j], 1)

for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

lcd.text("MASUKKAN PIN: ",1)

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    if countD > 0:
        countD = countD - 1
    GPIO.output(relay, 1)
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        GPIO.output(ledGreen, 0)
        GPIO.output(ledRed, 0)

	# keypad
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            countT = countT + 1

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_person[best_match_index]
                countD = countD + 3
                countT = 0

            print(name)
            print(f"dikenal = {countD} tDikenal = {countT}")
            face_names.append(name)
    
    for j in range(4):
        GPIO.output(COL[j], 0)
        for i in range(4):
             if GPIO.input(ROW[i]) == 0:
                 passEnter = passEnter + str(MATRIX[i][j])
                 print(MATRIX[i][j])
                 GPIO.output(buzzer, 1)
                 time.sleep(0.1)
                 GPIO.output(buzzer, 0)
                 passStars = passStars + "*"

                 if MATRIX[i][j] == "A":
                     passEnter = ""
                     passStars = ""
                 if MATRIX[i][j] == "D":
                     # wajah dan pin benar
                     if passEnter == password:
                         if countD >= 2 and countT == 0:
                             benar()
                             pause = True
                             while pause == True:
                                 if (GPIO.input(ROW[i])) == 0:
                                     pause = False 
                                     countD = 3
                                     break
                                 pass
                         if countT == 0 and countD <= 2:
                             noWajah()
                     # wajah salah pin benar
                     if passEnter == password and countT >= 2: 
                         tDikenal()
                         countT = 0
                         kirimWajah()
                     # pin salah
                     if passEnter != password:
                         pinSalah()
                         countSalah = countSalah + 1
                         if countSalah == 3:
                             kirimWajah()
                             countSalah = 0
                        
                     passEnter = ""
                     passStars = ""
                 time.sleep(0.1)
                 lcd.text("MASUKKAN PIN:",1)
                 GPIO.output(ledGreen, 0)
                 GPIO.output(ledRed, 0)
                 GPIO.output(buzzer, 0)

                 while(GPIO.input(ROW[i])) == 0:
                     pass

        time.sleep(0.01)
        lcd.text(passStars, 2)
        GPIO.output(COL[j],1)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 10, bottom - 10), font, 1.0, (0, 0, 0), 1)

    font = cv2.FONT_HERSHEY_DUPLEX
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
GPIO.cleanup()
lcd.clear()
