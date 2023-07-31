from PIL import Image, ImageDraw
from typing import Tuple
import numpy as np
import time
import cv2
import pandas as pd
import easydict
from pathlib import Path
import os
import torch

merge_df_tv = pd.read_csv('merge_df_tv.csv') # 4000개 데이터
df_warming = pd.read_csv('df_warming.csv') #4초
df_warming['code조합'] = df_warming['제품코드A'].astype(str) + ',' + df_warming['제품코드B'].astype(str)
df_warming['code조합'] = df_warming['code조합'].str.split(',')

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt', force_reload=True)  #2초
base_path = Path(os.getcwd())

def image_information(base_path):
    image_path = base_path.glob('images/*')
    img = sorted(image_path,reverse=True)[0] # 가장 최신에 들어온것 하나
    img = cv2.imread(str(img))
    results = model(img)
    df = results.pandas().xyxy[0] # 결과 데이터
    result = merge_df_tv[merge_df_tv['drug_N'].isin(df['name'])][['dl_name','dl_material','di_edi_code', '주성분', '효능','사용 방법', '주의사항', '주의음식', '부작용','di_class_no']]
    # print(set(result))
    for i,v in enumerate(df_warming['code조합']):
        if set(v).issubset(set(result['di_edi_code'].values))==True:
            print('문제 조합 : ' ,v ) # 문제 조합 
            print(result[result['di_edi_code']==v[0]]['dl_name'].values) # 문제조합 코드 이름 
            print(result[result['di_edi_code']==v[1]]['dl_name'].values) # 문제조합 코드 이름
            print('주의사항 : ' + df_warming.iloc[i]["상세정보"] + '이 생길수 있습니다') # 문제 조합 상세정보
image_information(base_path)