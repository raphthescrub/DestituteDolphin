import cv2
import numpy as np

net = cv2.dnn.readNet('yolov5s.onnx')
# String list that corresponds to the ID (0-79)

with open("classes.txt") as f:
    classes = [s.strip() for s in f.readlines()]
     
def main():
    global trash 
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        res, frame = cap.read()
        if not res: 
            continue
        process_frame(frame)
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
            if thisIsTrash(indexes, class_ids):
                x,y,w,h = [v*sf for v in boxes[i]] # extract the box values multiplied by the scale factor
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) # draw a blue box
                cv2.putText(frame, "trash",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
                
                
def thisIsTrash(indexes, class_ids):
    if classes[class_ids] == :
    
    
if __name__=="__main__": 
    main()