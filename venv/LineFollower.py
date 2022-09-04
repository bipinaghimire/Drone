import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# detecting white paper only
hsvVals = [0, 0, 117, 179, 22, 219]
sensors = 3
threshold =0.2

def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])

    mask = cv2.inRange(hsv, lower, upper)
    return mask

#finding edges in image
def getContours(imgThreshold, img):
    #external==outer edges
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = max(contours, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(biggest)
    cx = x + w//2
    cy = y + h//2
   
    cv2.drawContours(img, biggest, -1, (255, 0, 0), 7)
    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

def getSensorOutput(imgThreshold, sensors):
    imgs = np.hsplit(imgThreshold, sensors)
    totalpixels = img.shape[1] // sensors
    for x,im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold*totalpixels:
            return x
        cv2.imshow(str(x), im)
    cv2.imshow("Sensor 1", imgs[0])




while True:
    _, img = cap.read()
    img = cv2.resize(img, (480, 360))
    # img = cv2.flip(img, 1)

    imgThreshold = thresholding(img)

    cx = getContours(imgThreshold, img) ## for translation

    getSensorOutput(imgThreshold,sensors)
    cv2.imshow("Image", img)
    cv2.imshow("Path", imgThreshold)
    cv2.waitKey(1)