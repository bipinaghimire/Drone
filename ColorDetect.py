import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    
    if ret == False: 
        break
    
    frame = cv2.resize(frame,(750 ,700))
    
    #Extract required section from entire frame
    
    roiColor = cv2.rectangle(frame.copy(),(400, 365),(500, 435),(255,255,255),2) #For SampleTL.mp4 
    
    blcolor = (255, 0, 0)
    cv2.rectangle(frame, (400, 365),(500, 435), blcolor)
    
    hsv = cv2.cvtColor(roiColor,cv2.COLOR_BGR2HSV) 

    #red 
    lower_hsv_red = np.array([157,177,122]) 
    upper_hsv_red = np.array([179,255,255]) 
    mask_red = cv2.inRange(hsv,lowerb=lower_hsv_red,upperb=upper_hsv_red) 
    red_blur = cv2.medianBlur(mask_red, 7) 
    
    #green 
    lower_hsv_green = np.array([49,79,137])
    upper_hsv_green = np.array([90,255,255])
    mask_green = cv2.inRange(hsv,lowerb=lower_hsv_green,upperb=upper_hsv_green) 
    green_blur = cv2.medianBlur(mask_green, 7) 
    
    lower_hsv_yellow = np.array([15,150,150])
    upper_hsv_yellow = np.array([35,255,255])
    mask_yellow = cv2.inRange(hsv,lowerb=lower_hsv_yellow,upperb=upper_hsv_yellow)
    yellow_blur = cv2.medianBlur(mask_yellow, 7)
    
    #Because the image is a binary image, If the image has a white point, which is 255, then take his maximum max value 255 
    red_color = np.max(red_blur)
    green_color = np.max(green_blur)
    yellow_color = np.max(yellow_blur)
    
    if red_color == 255: 
        print('red') 
        cv2.rectangle(frame,(1020,50),(1060,90),(0,0,255),2 ) #Draw a rectangular frame by coordinates
        cv2.putText(frame, "red", (1020, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255),2) #red text information
    
    elif green_color == 255: 
        print('green') 
        cv2.rectangle(frame,(1020,50),(1060,90),(0,255 ,0),2) 
        cv2.putText(frame, "green", (1020, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),2)
    
    elif yellow_color == 255: 
        print('yellow') 
        cv2.rectangle(frame,(1020,50),(1060,90),(0,255 ,0),2) 
        cv2.putText(frame, "yellow", (1020, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0),2)
    else:
        print('no color')

    cv2.imshow('frame',frame) 
    red_blur = cv2.resize(red_blur,(300,200)) 
    green_blur = cv2.resize(green_blur,(300,200))
    yellow_blur = cv2.resize(yellow_blur, (300,200))
    
    #cv2.imshow('red_window',red_blur) 
    #cv2.imshow('green_window',green_blur) 
    #cv2.imshow('yellow_window',yellow_blur)
    
    c = cv2.waitKey(10) 
    if c==27: 
        break
    
cap.release()
cv2.destroyAllWindows() # destroy all opened windows