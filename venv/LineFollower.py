import cv2
import numpy as np
from djitellopy import tello

mydrone = tello.Tello()
mydrone.connect()
print(mydrone.get_battery())

mydrone.stream_on()
mydrone.takeoff()

cap = cv2.VideoCapture(0)
# detecting white paper only
hsvVals = [0, 0, 117, 179, 22, 219]
sensors = 3
threshold =0.2
width,height = 480,360
sensitivity = 3 # if number high less sensitive
weights =[-25,-15,0,15,25]

fspeed = 15

curve = 0
def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])

    mask = cv2.inRange(hsv, lower, upper)
    return mask

#finding edges in image
def getContours(imgThreshold, img):
    cx =0
    #external==outer edges
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(biggest)
        cx = x + w//2
        cy = y + h//2
   
        cv2.drawContours(img, biggest, -1, (255, 0, 0), 7)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

def getSensorOutput(imgThreshold, sensors):
    imgs = np.hsplit(imgThreshold, sensors)
    totalpixels = img.shape[1] // sensors * img.shape[0]
    senOut=[]
    for x,im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold*totalpixels:
            senOut.append(1)
        else:
            senOut.append(0)
        cv2.imshow(str(x), im)
    # cv2.imshow("Sensor 1", imgs[0])
    #print(senOut)
    return senOut

def sendCommands(senOut, cx):
    global curve
    ##translation
    lr = (cx -width//2)//sensitivity
    lr = int(np.clip(lr, -10, 10))
    if lr<2 and lr>-2:
        lr=0

    ##rotation
    if senOut == [1,0,0]:
        curve = weights[0]
    elif senOut == [1,1,0]:
        curve = weights[1]
    elif senOut == [0,1,0]:
        curve = weights[2]
    elif senOut == [0,1,1]:
        curve = weights[3]
    elif senOut == [0,0,1]:
        curve = weights[4]

    elif senOut == [0,0,0]:
        curve = weights[2]
    elif senOut == [1,1,1]:
        curve = weights[2]
    elif senOut == [1,0,1]:
        curve = weights[2]

    mydrone.send_rc_control(lr, fspeed, 0, curve)



while True:
    #_, img = cap.read()
    img = mydrone.get_frame_read()
    img = cv2.resize(img, (width, height))
    img = cv2.flip(img, 1)

    imgThreshold = thresholding(img)

    cx = getContours(imgThreshold, img) ## for translation

    senOut = getSensorOutput(imgThreshold,sensors)## for rotation
    sendCommands(senOut,cx)
    cv2.imshow("Image", img)
    cv2.imshow("Path", imgThreshold)
    cv2.waitKey(1)