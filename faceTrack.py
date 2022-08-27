from tracemalloc import start
from utilis import *
import cv2

w,h = 360,240

pid = [0.5,0.5,0]
pError = 0
pError_area = 0
startCounter = 0 # for no flight 1 - for flight 0 
myDrone = initialize_tello()

while True:
    #Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1
    # Get the frame from the drone
    img = telloGetFrame(myDrone,w,h)

    img, info = findFace(img)
    #print cx and cy of first face
    print(info[0][0])


    pError, pError_area = trackFace(myDrone, info, w, pid, pError_area)
    cv2.imshow('Image', img)
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break