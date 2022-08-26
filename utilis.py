from djitellopy import Tello
import cv2
import numpy as np

def initialize_tello():
    myDrone = Tello()
    myDrone.connect()

    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

#resizing the img
def telloGetFrame(myDrone, w =360, h =240):
    myframe = myDrone.get_frame_read()
    myframe = myframe.frame
    img = cv2.resize(myframe, (w, h))
    return img

def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#parameter is scale factor, how much the image size is reduced at each image scale and it is changeable
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)


    # for focusing in single face
    myFaceListC = []
    myFaceListArea = []
#drawing a rectangle around the face
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])

    if len(myFaceListArea) != 0:  
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]

    else:
        return img, [[0,0],0]

def trackFace(myDrone, info, w, pid, pError):
    #PID control==> smooth running of drone
    error = info[0][0] - w//2
    speed = pid[0]*error + pid[1]*(error - pError)# repeat these three line including area for forwad and backward & send speed down below
    #makes sure the drone doesn't go out of bounds
    speed = int(np.clip(speed, -100, 100))

    print(speed)
    #sending commands to drone
    if info[0][0] != 0:
        myDrone.yaw_velocity =speed
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error =0
#mathi ko set garya aba send garya
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity, 
        myDrone.for_back_velocity, myDrone.up_down_velocity, 
        myDrone.yaw_velocity)

    return error