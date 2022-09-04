from djitellopy import tello
from time import sleep

mydrone = tello.Tello()
mydrone.connect()
print(mydrone.get_battery())

mydrone.takeoff()

mydrone.send_rc_control(0, 0, 0, 0)
sleep(1)
mydrone.send_rc_control(0, 20, 0, 0)
sleep(1)
mydrone.send_rc_control(0, 0, 0, 0)
sleep(1)
mydrone.land()
