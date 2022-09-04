import cv2
import face_recognition
import sys

# pip intsall numpy, cmake, dlib, face-recognition

def take_picture():
    print("Face scan")
    cap= cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite('T1.jpg',frame)
    cv2.destroyAllWindows()
    cap.release()
    print("Scan Complete")

def analyze_user():
    print("Analyzing User")
    known_image = face_recognition.load_image_file("T1.jpg")
    known_image = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)

    #find face
    myface = face_recognition.face_locations(known_image)[0]
    #encode face
    encode = face_recognition.face_encodings(known_image)[0]
    cv2.rectangle(known_image, (myface[3], myface[0]), (myface[1], myface[2]), (255, 0, 255), 2)

    sampleimg = face_recognition.load_image_file("T2.jpg")
    sampleimg = cv2.cvtColor(sampleimg, cv2.COLOR_BGR2RGB)

    # sampleface = face_recognition.face_locations(sampleimg)[0]
    try:
        sampleface = face_recognition.face_locations(sampleimg)[0]
        encode2 = face_recognition.face_encodings(sampleimg)[0]
    except IndexError as e:
        print("No face detected")
        sys.exit()

    cv2.rectangle(sampleimg, (sampleface[3], sampleface[0]), (sampleface[1], sampleface[2]), (255, 0, 255), 2)
    cv2.imshow("Sample", sampleimg)
    cv2.waitKey(0)
    
    result = face_recognition.compare_faces([encode], encode2)
    resultString = str(result)

    if resultString == "[True]":
        print("Access Granted")
    else:
        print("Access Denied")

take_picture()
analyze_user()



