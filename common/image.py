import cv2
from common.utils import timeit
from glob import glob
import numpy as np

@timeit
def resize_image(path):
    path_list = glob(str(path / '*.png'))
    for img_path in path_list:
        img = cv2.imread(str(img_path))
        cropped_img = img[320:960, 168:808]
        cv2.imwrite(img_path, cropped_img)
        
def show_img(image, contours): 
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour) # 딱 맞는 사각형 좌표 
        #bounding_rects.append((x/1280, y/976, (x + w)/1280, (y + h)/976)) # 사각형 그릴떄 쓰는 좌표 
    
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,200,0),2) # 사각형 그림 
    cv2.drawContours(image,contours,-1,(0,200,0))
    cv2.imshow('contour',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

@timeit
def get_contour(path):
    path_list = glob(str(path / '*.png'))
    bounding_rects =np.array([[0, 0, 0, 0] for _ in path_list]) # 좌표 담는 리스트 
    # square_rects = []
    result = []  # 종류 + 좌표 담는 리스트 
    for i, img_path in enumerate(path_list): # file_list_png는 png데이터가 있는 파일 
        img = cv2.imread(str(img_path)) # 읽기

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #gray
        blurred_img = cv2.GaussianBlur(gray_img, (5, 5),0) # blur처리
        ret, otsu = cv2.threshold(blurred_img,-1,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU) #otsu최적화 
        contours , hierarchy = cv2.findContours(otsu,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE) #윤곽추출
        test_img = cv2.drawContours(img, contours, 0, 2)
        show_img(img, contours)
        x, y, w, h = cv2.boundingRect(np.array(contours[1])) # 딱 맞는 사각형 좌표 
        bounding_rects[i]=[x/1280, y/976, (x+w)/1280, (y+h)/976] # 사각형 그릴떄 쓰는 좌표 
        #print(bounding_rects[i])
        break
            #square_rects.append(((x,y),(x+w,y),(x,y+h),(x+w,y+h))) # 4개 꼭지점 좌표 
    #     for i in range(len(bounding_rects)): 
    #         result.append((name_lst[i],) + bounding_rects[i] )
                
    # return result
