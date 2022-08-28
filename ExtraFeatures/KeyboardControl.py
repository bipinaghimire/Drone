from djitellopy import tello
import KeyPressModule as kp
from time import sleep

kp.init()
myDrone = tello.Tello()
myDrone.connect()

print(myDrone.get_battery())

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
        yv = myDrone.land()
    if kp.getKey("e"):
        yv = myDrone.takeoff()

    return [lr, fb, ud, yv]


while True:
    values = getKeyboardInput()
    myDrone.send_rc_control(values[0], values[1], values[2], values[3])
    sleep(0.1)
    