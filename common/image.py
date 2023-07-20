import cv2
from common.utils import timeit
from glob import glob
import numpy as np
import pandas as pd
from common.params import args
import os
import json

from common.multiprocessing import process_images, chunk
from multiprocessing import Process
from multiprocessing import cpu_count

@timeit
def resize_image(path, label_info, pad = args.im_padding):
    path_list = sorted(path.glob('*.png'))
    for i, img_path in enumerate(path_list):
        _, file_name = os.path.split(img_path)
        img = cv2.imread(str(img_path))
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        x, y, w, h = json.loads(label_info['bbox'].loc[label_info['file_name']==file_name].iloc[0])
        img = img[(y//2)-pad:(y//2)+(h//2)+pad, 
                  (x//2)-pad:(x//2)+(w//2)+pad]
        cv2.imwrite(str(img_path), img)

def resize_image_m(img_path, i, label_info, pad = args.im_padding):
    _, file_name = os.path.split(img_path)
    if file_name != label_info.iloc[i]['file_name']:
        print('File name mismatch!')
        return None
    img = cv2.imread(str(img_path))
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    x, y, w, h = json.loads(label_info['bbox'][i])
    img = img[(y//2)-pad:(y//2)+(h//2)+pad, 
                (x//2)-pad:(x//2)+(w//2)+pad]
    cv2.imwrite(str(args.data_path / f'processed/{file_name}'), img)

@timeit
def multiprocess(path):
    label_info = pd.read_csv(args.data_path / 'db/annotations.csv')
    for i, input_path in enumerate(sorted(path.rglob('*.png'))):
        p = Process(target=resize_image_m, args=(input_path,i,label_info,))
        p.start()

def show_img(image, contours): 
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour) # 딱 맞는 사각형 좌표 
        #bounding_rects.append((x/1280, y/976, (x + w)/1280, (y + h)/976)) # 사각형 그릴떄 쓰는 좌표 
    
    cv2.rectangle(image,(x,y,w,h),(0,200,0),2) # 사각형 그림 
    cv2.drawContours(image,contours,-1,(0,200,0))
    cv2.imshow('contour',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

@timeit
def get_contour(path):
    path_list = path.rglob('*')
    for paths in path_list:
        png_path = paths.glob('**/*.png')
        # path_list = glob(str(path / '*.png'))
        # bounding_rects =np.array([[0, 0, 0, 0] for _ in path_list]) # 좌표 담는 리스트 
        bounding_rects = []
        textfile =pd.read_csv(args.data_path / 'db/annotations.csv')
    # square_rects = []
        result = []  # 종류 + 좌표 담는 리스트 
        for i, img_path in enumerate(png_path): # file_list_png는 png데이터가 있는 파일 
            print(f'-------------------------{i}----------------------------')
            file_name = str(img_path).split('\\')[-1].split('.')[0]#파일 이름 저장
            img = cv2.imread(str(img_path)) # 읽기
            img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #gray
            
            blur = cv2.GaussianBlur(gray_img, ksize=(5,5), sigmaX=0)
            # edged = cv2.Canny(blur, 10, 100)
            
            capsul = textfile[textfile['form_code_name'].str.contains('캡슐')]
            capsul.reset_index(drop=True,inplace=True)

            if capsul['file_name'][i].split('.')[0] == file_name: #form_code_name에 캡슐이 들어가는 것들만 따로 처리
                edged = cv2.Canny(blur, 10, 100)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
                result = cv2.dilate(edged, kernel, iterations = 3)
                closed = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
                ret, thresh = cv2.threshold(closed,127,255,0)
                contours, hierachy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            else :
                edged = cv2.Canny(blur, 10, 200)
                ret, otsu = cv2.threshold(edged,-1,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU) #otsu최적화 
                contours , hierarchy = cv2.findContours(otsu,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE) #윤곽추출
            # x, y, w, h = cv2.boundingRect(np.array(contours[0])) # 딱 맞는 사각형 좌표 
            # bounding_rects[i]=[x/1280, y/976, (x+w)/1280, (y+h)/976] # 사각형 그릴떄 쓰는 좌표 
            # print(bounding_rects[i])
            contours_xy = np.array(contours)
            # x의 min과 max 찾기
            x_min, x_max = 0,0
            value = list()
            for i in range(len(contours_xy)):
                for j in range(len(contours_xy[i])):
                    value.append(contours_xy[i][j][0][0]) #네번째 괄호가 0일때 x의 값
                    x_min = min(value)
                    x_max = max(value)

            # y의 min과 max 찾기
            y_min, y_max = 0,0
            value = list()
            for i in range(len(contours_xy)):
                for j in range(len(contours_xy[i])):
                    value.append(contours_xy[i][j][0][1]) #네번째 괄호가 0일때 x의 값
                    y_min = min(value)
                    y_max = max(value)

            # image trim 하기
            x = x_min
            y = y_min
            w = x_max-x_min
            h = y_max-y_min
            # for contour in contours:
            #     x, y, w, h = cv2.boundingRect(contour) # 딱 맞는 사각형 좌표 
                # bounding_rects.append((x/1280, y/976, (x + w)/1280, (y + h)/976)) # 사각형 그릴떄 쓰는 좌표 
            # dot = [((x-((976-640)/2))+(w/2)), ((y-((1280-640)/2))+(h/2)), w, h]
            dot = [((x+((976-640)/2))), ((y+((1280-640)/2))), w, h]
            print(dot)
            show_img(img,contours)
            print(x, y, w, h)
            break
        #square_rects.append(((x,y),(x+w,y),(x,y+h),(x+w,y+h))) # 4개 꼭지점 좌표 
    #     for i in range(len(bounding_rects)): 
    #         result.append((name_lst[i],) + bounding_rects[i] )
            
    # return result