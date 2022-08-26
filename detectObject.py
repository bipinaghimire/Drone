# pip install tensorflow
#pip install opencv-python
#pip install keras
#pip install imageAI
from imageAI.Detection import ObjectDetection

detector = ObjectDetection()

model_path = "./models/yolo-tiny.h5"
input_path = "./input/1t.jpg"
output_path = "./output/newimage.jpg"

detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()
detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)

for eachItem in detection:
    print(eachItem["name"] , " : ", eachItem["percentage_probability"])