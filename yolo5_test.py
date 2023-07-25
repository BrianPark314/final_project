import cv2, sys
from matplotlib import pyplot as plt
import numpy as np
import os
import json, pandas as pd



###############  경로나 이미 짜여진 코드에서 중복되어있는게 많으니까 그냥 흐름만 확인하고 test파일 생성만 해주면됨. ##################################


def save_file_at_dir(dir_path, filename, file_content, mode='w'): #폴더 없으면 생성해주고 txt파일 생성
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, filename), mode) as f:
        f.write(file_content)
        f.close()

path2 = './dataset1/'
path3 = './dataset1_label/'
cunt = 0
cunts = 0
cnt1 = 0
cnt2 = 0

imagePaths2 = [os.path.join(path2,f) for f in os.listdir(path2)] #이미지 파일 경로
imagePaths3 = [os.path.join(path3,f) for f in os.listdir(path3)] #좌표 파일 경로

###############  for문 2번쓴 이유는 그냥 일단 테스트 위해서 돌려봤고,
###############  2개로 만든이유는 그냥 이미지 파일생성하고 json에서 좌표값 따로 뽑아서 동일 폴더에 저장해주려고 따로 돌림.
for imagePath1 in imagePaths3:
    cunts += 1
    for filename in os.listdir(imagePath1): #각 파일마다
        cnt2 += 1
        with open(f'{imagePath1}/{filename}','rt', encoding='UTF8') as f:
            js = json.loads(f.read()) ## json 라이브러리 이용
        df = pd.DataFrame(js)
        x,y,w,h =  df['annotations'][0]['bbox']
        dot = [(cunts-1), ((x-((976-640)/2))+(w/2))/640, ((y-((1280-640)/2))+(h/2))/640, w/640, h/640] #좌표값 상대 좌표로 변환
        result = ' '.join(str(s) for s in dot)

        if cnt2 <= 100 :
            save_file_at_dir(f'{path2}testlabel', f"{filename.strip('.json')}.txt", result) #이미지 파일 명이랑 텍스트 파일 명이랑 1:1 매칭이되어야하기때문에 이미지 파일명에 txt 만 수정하여 상대좌표값 입력
        else :
            save_file_at_dir(f'{path2}validlabel', f"{filename.strip('.json')}.txt", result)
        if cnt2 == 120:
            cnt2 = 0
            break

for imagePath in imagePaths2:
    cunt += 1
    for filename in os.listdir(imagePath): #각 파일마다
        cnt1 += 1
        image = cv2.imread(f'{imagePath}/{filename}')
        crop_img = image[320:960,168:808]

        if cnt1 <= 100 :#파일이름
            cv2.imwrite(f'{path2}testlabel/{filename}', crop_img) #파일이름
        else :
            cv2.imwrite(f'{path2}validlabel/{filename}', crop_img)
        if cnt1 == 120:
            cnt1 = 0
            break

        # cv2.rectangle(image,(x,y),(x+w,y+h),(0,200,0),2) # 사각형 그림 
