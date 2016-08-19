import sys
import numpy as np
import cv2

try :
    samples =  np.empty((0, 100))
    responses = []
    keys = [i for i in range(48, 58)] # range of keypad
    
    for i in range(1,20): # 20 is maximum samples in the directory
        image = cv2.imread('samples/' + str(i) + '.jpg')
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        lower = np.array([28, 0, 0]) # lower hsv of numbers
        upper = np.array([255, 19, 47]) # upper hsv of numbers
        thresh = cv2.inRange(image, lower, upper)
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel) 
        
        backupt = thresh.copy()        
        
        _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:     
                [x, y, w, h] = cv2.boundingRect(contour)            
                if h > 1 :                
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)                
                    roi = backupt[y:y+h, x:x+w]
                    roi_small = cv2.resize(roi, (10, 10))
                    cv2.imshow('norm', roi_small)
                    key = cv2.waitKey(0)
                    key = key - 1114032 + 48 # the number that you will be enter !
                    print str(x) + " , " + str(y) + " , " + str(w) + " , " + str(h) + " : " + str(key)                    
                    if key == 27:
                        sys.exit()
                    elif key in keys:                
                        sample = roi_small.reshape((1,100))
                        samples = np.append(samples,sample,0)
                        responses.append(int(chr(key)))
                    else :
                        continue
    
    print "training complete"
    np.savetxt('general-samples.data', samples)
    responses = np.array(responses, np.float32)
    responses = responses.reshape((responses.size,1))
    np.savetxt('general-responses.data', responses) 
except KeyboardInterrupt:
    pass
