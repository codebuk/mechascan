__author__ = 'dan'

__author__ = 'dan'

import numpy as np
import copy
import cv2

IMG_IN = '/home/dan/Documents/2/65.jpg'

# keep a copy of original image
original = cv2.imread(IMG_IN)

# Read the image, convert it into grayscale, and make in binary image for threshold value of 1.
#cv2.CV_LOAD_IMAGE_GRAYSCALE
img = cv2.imread(IMG_IN,0)

# use binary threshold, all pixel that are beyond 3 are made white
_, thresh_original = cv2.threshold(img, 3, 255, cv2.THRESH_BINARY)

# Now find contours in it.
thresh = copy.copy(thresh_original)
z, contours, y = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# get contours with highest height
lst_contours = []
for cnt in contours:
    #print ('c')
    #print (cnt)
    ctr = cv2.boundingRect(cnt)
    #print ( ctr)
    lst_contours.append(ctr)
x,y,w,h = sorted(lst_contours, key=lambda coef: coef[3])[-1]

print (x,y,w,h)

crop = original[y:y+h,x:x+w]
cv2.imwrite('sofwinres.png',crop)

import os
rootdir = '/home/dan/Documents/2/'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print (os.path.join(subdir, file))


        if i.endswith(".asm") or i.endswith(".py"):
