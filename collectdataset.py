import sys
import os

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import copy
import cv2





    # Feed the image_data as input to the graph and get first prediction

c = 0

cap = cv2.VideoCapture(0)

res, score = '', 0.0
i = 0
mem = ''
consecutive = 0
sequence = ''
    
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    if ret:
        x1, y1, x2, y2 = 100, 100, 300, 300
        img_cropped = img[y1:y2, x1:x2]

        c += 1
        print(c)
        #image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
        cv2.imwrite( "imagine" + str(c) + ".jpg", img_cropped)
        a = cv2.waitKey(1) # waits to see if `esc` is pressed
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.imshow("img", img)
        if a == 27: # when `esc` is pressed
            break


cv2.destroyAllWindows() 
cv2.VideoCapture(0).release()
