import cv2
import numpy as np

net = cv2.dnn.readNet('yolov5s.onnx')
# String list 

with open("classes.txt") as f:
    classes = [s.strip() for s in f.readlines()]
     
def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        res, frame = cap.read()
        if not res: 
            continue
        process_frame(frame)
        cv2.imshow("Is this Trash??", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    
def process_frame(frame):
    blob1 = format_yolov5(frame)
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
    draw_boxes(frame,boxes,indexes,class_ids)
    
def format_yolov5(frame):
    col, row, _ = frame.shape 
    _max = max(col, row) # get the maximum dimension
    resized = np.zeros((_max, _max, 3), np.uint8) # create a new square frame
    resized[0:col, 0:row] = frame # insert the original image at the top left
    result = cv2.dnn.blobFromImage(resized, 1/255.0, (640, 640), swapRB=True)
    return result

def draw_boxes(frame,boxes,indexes,class_ids):
    
    sf = int(max(frame.shape[0],frame.shape[1])/640) # determine the scale factor to convert back
    for i in range (len(boxes)):
        if i in indexes: 
            if thisIsTrash(class_ids[i]):
                x,y,w,h = [v*sf for v in boxes[i]] # extract the box values multiplied by the scale factor
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) # draw a blue box
                cv2.putText(frame, "trash",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))          
                
def thisIsTrash(class_ids):
    index = classes[class_ids]
    trash = True
    notTrashItems = ['person', 'bicycle', 'car', 'motorbike', 
                'aeroplane', 'bus', 'train', 'truck', 'boat', 
                'traffic light', 'fire hydrant', 'stop sign', 
                'parking meter', 'bench', 'bird', 'cat', 'dog',
                'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
                'giraffe', 'surfboard', 'chair', 'sofa']
    
    for i in notTrashItems:
        if (i == index):
            trash = False
            break
        
    return trash
       
    
if __name__=="__main__": 
    main()