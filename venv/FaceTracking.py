from time import time
import cv2
import numpy as np

from djitellopy import tello
mydrone = tello.Tello()
mydrone.connect()
print(mydrone.get_battery())

mydrone.stream_on()
mydrone.takeoff() 
mydrone.send_rc_control(0, 0, 25, 0)
time.sleep(2.2)

w,h=360,240
cap = cv2.VideoCapture(0)
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

def findFace(img):
    face_cascade = cv2.CascadeClassifier('Resources/hFrontalFace.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 8)
    
    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace(info, w,pid,pError):
    area = info[1]

    x,y = info[0]
    fb = 0

    error = x - w//2
    speed = pid[0]*error + pid[1]*(error-pError)
    speed = int(np.clip(speed, -100, 100))
    #stay stationary 
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    #too close move back
    elif area>fbRange[1]:
        fb = -20
    elif area<fbRange[0] and area!=0:
        fb = 20


    if x == 0:
        speed = 0
        error = 0
    
        # print(speed,fb)

    mydrone.send_rc_control(0, fb, 0, speed)
    return error


while True:
    #code to run web cam of laptop 1,2,4 8,9,10 samma
    #8
    # _, img = cap.read()
    img = mydrone.get_frame_read()
    #not find face
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError=trackFace( info, w,pid,pError)
    # print("Area: ", info[1],"Center: ", info[0])

    #9
    cv2.imshow("Webcam", img)
    #10
    if cv2.waitKey(1) & 0xFF == ord('q'):
        mydrone.land()
        break