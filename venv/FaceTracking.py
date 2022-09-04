import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fbRange = [6200, 6800]

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

def tracFace(img, myFaceList, w,pid,pError):
    area = info[1]
    #stay stationary
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    #too close move back
    if area>fbRange[1]:
        fb = -20
    elif area<fbRange[0] and area!=0:
        fb = 20
    



while True:
    #code to run web cam of laptop 1,2,4 8,9,10 samma
    #8
    _, img = cap.read()
    #not find face
    img, info = findFace(img)
    # print("Area: ", info[1],"Center: ", info[0])

    #9
    cv2.imshow("Webcam", img)
    #10
    cv2.waitKey(1)