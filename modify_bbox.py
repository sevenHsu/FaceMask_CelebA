import os
import cv2
import glob
import tqdm
import random
import numpy as np
from PIL import Image,ImageDraw
img_dir = 'Img/img_align_celeba'
sav_dir = 'CelebA_bbox'
imglist_path = 'Anno/list_landmarks_align_celeba.txt'

def get_ratio(l,c,r):
    return c-l,r-c
with open(imglist_path,'r') as f:
    lines = f.read().splitlines()
fw = open("Anno/list_modify_bbox_align_celeba.txt",'w')
fw.write("%s\nx1 y1 x2 y2\n"%str(len(lines)-2))

for line in tqdm.tqdm(lines[2:]):
    line=line.split()
    imgpath = os.path.join(img_dir,line[0])
    img = cv2.imread(imgpath)
    imgh,imgw,_=img.shape
    points = np.array(list(map(int,line[1:]))).reshape([-1,2])
    l,r = get_ratio(points[3,0],points[2,0],points[4,0])
    min_x,min_y,min_w,min_h = cv2.boundingRect(points)
    min_cx,min_cy = min_x+min_w/2,min_y+min_h/2
    min_x1,min_y1,min_x2,min_y2 = min_x,min_y,min_x+min_w,min_y+min_h
    nose = points[2]
    if l<0:
        x1, x2= min_x1-min_w*0.2,min_cx+2.1*min_w
    elif r<0:
        x1, x2 =min_cx - 2.1*min_w,min_x2+0.2*min_w
    else: 
        x1,x2=nose[0]-min_w*(abs(nose[0]-min_x1)*2/min_w),nose[0]+min_w*(abs(min_x2-nose[0])*2/min_w)

    x1,y1,x2,y2 = map(lambda x:int(x),[x1,min_cy-min_h*1.1,x2,min_cy+min_h*1.1])
    x1 = max(1,x1)
    y1 = max(1,y1)
    x2 = min(x2,imgw-2)
    y2 = min(y2,imgh-2)

    fw.write("%s "%line[0]+' '.join(map(str,[x1,y1,x2,y2]))+'\n')
    #y1 = int(y1-faceh*0.1)
    #y2 = int(y2+faceh*0.1)
    #cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
    #cv2.imwrite(os.path.join(sav_dir,line[0]),img)
fw.close()
