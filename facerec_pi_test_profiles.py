#Modified by smartbuilds.io
#Date: 03.07.20
#Desc: This script is running a face recongition of a live webcam stream. This is a modifed
#code of the orginal Ageitgey (GitHub) face recognition demo to include multiple faces.
#Simply add the your desired 'passport-style' face to the 'profiles' folder.

#test lcd
from rpi_lcd import LCD
import RPi.GPIO as GPIO

import face_recognition
import cv2
import numpy as np
import os
import time


#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

# Note: This script requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# Visit smartbuids.io for more information

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

#LCD object
lcd = LCD()
#Store objects in array
known_person=[] #Name of person string
known_image=[] #Image object
known_face_encodings=[] #Encoding object

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

prev_frame_time = 0
new_frame_time = 0

lcd.text("initializing...", 1)

#Loop to add images in friends folder
for file in os.listdir("src/profiles"):
    try:
        #Extracting person name from the image filename eg: david.jpg
        known_person.append(file.replace(".jpg", ""))
        file=os.path.join("src/profiles/", file)
        known_image = face_recognition.load_image_file(file)
        #print(face_recognition.face_encodings(known_image)[0])
        known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
        #print(known_face_encodings)

    except Exception as e:
        pass
    
#print(len(known_face_encodings))
#print(known_person)

        
lcd.clear()

while True:
    	
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    fps = str(fps)
	#lcd
    lcd.text(f"FPS : {fps}", 2)
   # lcd.text("",1)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        GPIO.output(21, 1)
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            #print(face_encoding)
            #print(matches)

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_person[best_match_index]
                GPIO.output(21, 0)
                time.sleep(3)

            print(name)
            lcd.text(f"     {name}    ", 1)
            
            #print(face_locations)
            face_names.append(name)
   
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
    cv2.putText(frame, fps, (7, 70), font, 3, (232, 230, 230), 3, cv2.LINE_AA)
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
