# 일반적 boundingbox 시도
import cv2
import numpy as np
import random
from pathlib import Path
path = Path('C:/Users/User/Documents/final_project/validlabel')

bounding_rects =[]
square_rects = []

for img in file_list_png:
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray, (5, 5),0)
    ret, thresh = cv2.threshold(blurred_img,127,255,0) 
    contours , hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    largest_contour = max(contour, key=cv2.contourArea)
    
    for contour in contours:
        largest_contour = max(contour, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour) # 딱 맞는 사각형 좌표 
        bounding_rects.append((x/1280, y/976, (x + w)/1280, (y + h)/976)) # 사각형 그릴떄 쓰는 좌표 
        # square_rects.append(((x,y),(x+w,y),(x,y+h),(x+w,y+h))) # 4개 꼭지점 좌표 
    break

cv2.rectangle(image,(x,y),(x+w,y+h),(0,200,0),2) # 사각형 그림 
cv2.drawContours(image,contours,-1,(0,200,0))
cv2.imshow('contour',image)
cv2.waitKey(0)
cv2.destroyAllWindows()