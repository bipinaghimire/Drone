import imp
from djitellopy import tello
import KeyPressModule as kp
import time
from time import sleep
import cv2

kp.init()
mydrone = tello.Tello()
mydrone.connect()

global img

print(mydrone.get_battery())

mydrone.stream_on()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed =50
    if kp.getKey("Left"):
        lr = -speed
    elif kp.getKey("Right"):
        lr = speed

    if kp.getKey("Up"):
        fb = speed
    elif kp.getKey("Down"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = speed
    elif kp.getKey("d"):
        yv = -speed

    if kp.getKey("q"):
        yv = mydrone.land()
    if kp.getKey("e"):
        yv = mydrone.takeoff()

    if kp.getKey("z"):
        cv2.imwrite("Resources/Image/"+str(int(time.time()))+".jpg", img)
        time.sleep(0.5)
    return [lr, fb, ud, yv]


while True:
    values = getKeyboardInput()
    mydrone.send_rc_control(values[0], values[1], values[2], values[3])

    img = mydrone.get_frame_read()
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Drone", img)
    cv2.waitKey(1)
    sleep(0.1)