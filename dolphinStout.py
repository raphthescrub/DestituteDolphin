import cv2
import numpy as np
import argparse


with open("classes.txt") as f:
        classes = [s.strip() for s in f.readlines()]
        
def checkIfPerson(image):
    net = cv2.dnn.readNet('yolov5s.onnx')
    blob1 = format_yolov5(image)
    net.setInput(blob1)
    predictions1 = net.forward()
    output = predictions1[0]
    boxes = []
    confidences = []
    class_ids = [] 
    for row in output: # each row in the output is one box, xc,yc,w,h,conf,80 class probabilities
        if row[4] > .5: # we only keep boxes with good confidence
            xc, yc, w, h = row[0], row[1], row[2], row[3] # note, these are in 640x640 space
            max_index = cv2.minMaxLoc(row[4:])[3][1] # this will figure out the highest probability class
            class_ids.append(max_index) 
            left = int(xc-w/2) # the boxes are in center coordinates, so move by half width                            
            top = int(yc-h/2) 
            width = int(w)
            height = int(h) 
            confidences.append(row[4])
            boxes.append([left,top,width,height]) 
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)
    draw_boxes(image,boxes,indexes,class_ids)
    
def format_yolov5(image):
    col, row, _ = image.shape 
    _max = max(col, row) # get the maximum dimension
    resized = np.zeros((_max, _max, 3), np.uint8) # create a new square frame
    resized[0:col, 0:row] = image # insert the original image at the top left
    result = cv2.dnn.blobFromImage(resized, 1/255.0, (640, 640), swapRB=True)
    return result

def draw_boxes(image,boxes,indexes,class_ids):
    sf = int(max(image.shape[0],image.shape[1])/640) # determine the scale factor to convert back
    for i in range (len(boxes)):
        if i in indexes: 
            if thisPerson(class_ids[i]):
                x,y,w,h = [v*sf for v in boxes[i]] # extract the box values multiplied by the scale factor
                cv2.rectangle(image,(x,y),(x+w,y+h),(140,0,140),2) # draw a blue box
                cv2.putText(image, '"Dolphin"',(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,0))          
                
def thisPerson(class_ids):
    if classes[class_ids] == 'person':
        return True

ap = argparse.ArgumentParser()
ap.add_argument("-v", "-video", required = True, help="path to input video file")
ap.add_argument("-o", "-output", required = True, help="path to output 'long exposure'")


print("[Info] opening video file pointer...")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

cap.set(cv2.CAP_PROP_EXPOSURE, -4)

while True:
    ret, img = cap.read()
    
    brightness = np.sum(img) / (255 * 1280 * 1024)
    
    minimum_brightness = 0.66
    ratio = brightness / minimum_brightness
    if ratio >= 1:
        print("Image already bright")
        bright_img = img
    
    else: 
        bright_img = cv2.convertScaleAbs(img, alpha = 1, beta = 255 * (minimum_brightness - brightness))
    
    gray = cv2.cvtColor(bright_img, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    gray = cv2.GaussianBlur(gray, (41, 41), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    image = bright_img.copy()
    # cv2.circle(bright_img, mmscLoc, 10, (255, 0, 0), 2)
    cv2.circle(image, minLoc, 100, (255, 0, 0), 2)
    # display the results of the naive attempt
    
    checkIfPerson(image)
    cv2.imshow("image", image)
    
    if cv2.waitKey(1) == ord('q'):
        break