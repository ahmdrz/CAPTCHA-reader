import cv2
import numpy as np
import sys

if len(sys.argv) != 2 :
    print "Usage classify <file>"
    sys.exit()
    
print "File name : " + sys.argv[1]

def getKey(item):
    [x, y, w, h] = cv2.boundingRect(item)
    return x

samples = np.loadtxt('general-samples.data', np.float32)
responses = np.loadtxt('general-responses.data', np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.ml.KNearest_create()
model.train(samples,cv2.ml.ROW_SAMPLE, responses)

image = cv2.imread(sys.argv[1])
hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

lower = np.array([28, 0, 0]) # lower hsv range
upper = np.array([255, 19, 47]) # upper hsv range

thresh = cv2.inRange(image, lower, upper)
kernel = np.ones((3, 3), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
backupt = thresh.copy()                
_,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours,key=getKey)
string = ""

for contour in contours:
    if cv2.contourArea(contour) > 5:        
        [x, y, w, h] = cv2.boundingRect(contour)
        if  h > 1:                        
            roi = backupt[y:y+h, x:x+w]
            roi_small = cv2.resize(roi,(10,10))
            roi_small = roi_small.reshape((1,100))
            roi_small = np.float32(roi_small)            
            retval, results, neigh_resp, dists = model.findNearest(roi_small
                    , k = 1)            
            string += str(int((results[0][0])))            

print "The number is : " + string            
cv2.imshow('im',image)
cv2.waitKey(0)