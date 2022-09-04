from djitellopy import tello
import cv2
mydrone = tello.Tello()
mydrone.connect()
print(mydrone.get_battery())

mydrone.stream_on()
while True:
    img = mydrone.get_frame_read()
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Drone", img)
    cv2.waitKey(1)