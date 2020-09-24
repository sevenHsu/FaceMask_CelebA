from PIL import Image
import numpy as np
import glob
import cv2

imgpaths = glob.glob("./*png")
for imgpath in imgpaths:
    img = Image.open(imgpath)
    img = np.array(img)
    gray = np.mean(img[:,:,:3])*np.where(img[:,:,3]>0,1,0)#cv2.cvtColor(img,cv2.COLOR_RGBA2GRAY)
    gray = gray.astype(np.uint8)
    ret,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contour = np.concatenate(contours)
    x1,y1,w,h = cv2.boundingRect(contour)
    x1,y1,x2,y2 = x1,y1,x1+w,y1+h
    img = img[y1:y2,x1:x2]
    img = Image.fromarray(img)
    img.save(imgpath)
     
