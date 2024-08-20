import numpy as np
import cv2
import os

# made by A Mohammed Faazil

def object_detection(image_path):

    prototxt_path = r"model\MobileNetSSD_deploy.prototxt"
    model_path = r"model\MobileNetSSD_deploy.caffemodel"
    min_confidence = 0.3

    classes = [
        "background",  
        "aeroplane",
        "bicycle",
        "bird",
        "boat",
        "bottle",
        "bus",
        "car",
        "cat",
        "chair",
        "cow",
        "dining table",
        "dog",
        "horse",
        "motorbike",
        "person",
        "potted plant",
        "sheep",
        "sofa",
        "train",
        "tv/monitor"]

    np.random.seed(543210)
    colors = np.random.uniform(0,255,size = (len(classes),3))

    net = cv2.dnn.readNetFromCaffe(prototxt_path,model_path)

    image = cv2.imread(image_path)
    height,width = image.shape[0],image.shape[1]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (500, 500)), 0.007843, (500, 500), 127.5)
    
    net.setInput(blob)
    detected_objects = net.forward()


    for i in range(detected_objects.shape[2]):
        confidence = detected_objects[0][0][i][2]
        
        if confidence >  min_confidence:
            class_index = int(detected_objects[0,0,i,1])

            upper_left_x = int(detected_objects[0,0,i,3] * width)
            upper_left_y = int(detected_objects[0,0,i,4] * height)
            lower_left_x = int(detected_objects[0,0,i,5] * width)
            lower_left_y = int(detected_objects[0,0,i,6] * height)

            prediction_text = f"{classes[class_index]} : {confidence:.2f}%"
            cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_left_x,lower_left_y), colors[class_index],3)
            cv2.putText(image, prediction_text, (upper_left_x,upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15) ,
                        cv2.FONT_HERSHEY_SIMPLEX,0.6, colors[class_index],2)





    cv2.imshow("Detected Objects",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


folder_path = r'C:\Desktop\codeclause_internship\object_detection\images'

for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        file_path = file_path.replace('\\', '/')
    
        if filename.lower().endswith(('.jpg', '.png')):
           object_detection(file_path)
