from common.params import args
import time
import orjson
import json
import os
import pandas as pd
from pathlib import Path
import gc
import splitfolders
from glob import glob
import shutil
import os.path
from os import path
from common.utils import timeit

@timeit
def image_path_move(): #이미지 옮기는 함수
    basic_path = args.data_path / 'train/final_data/val'
    path_list = basic_path.rglob('*.png')
    for paths in path_list:
        shutil.move(str(paths), basic_path)

@timeit
def label_path_move(): #라벨 옮기는 함수
    dest_path = args.data_path/'train/final_data2/val'
    src_path = args.data_path/'train/labels7'
    for paths in dest_path:
        file_name = str(paths).split('\\')[-1].split('.')[0]
        shutil.copy(src_path/f'{file_name}.txt',dest_path/f'{file_name}.txt')

@timeit
def train_image_label_redivide(): #학습이미지 라벨 200개로 맞춰서 나눴기때문에 파일명과 라벨명 매치하여 분리해주는 함수
    label_list = pd.read_csv(args.data_path / 'db/label_list.csv',encoding='utf-8')
    path_label = label_list['id'].unique()
    total_path = args.data_path/'train/final_data'
    dest_path = args.data_path/'train/final_data3'
    total_list = total_path.rglob('*')
    i = 0
    for paths1 in path_label:
        for paths2 in total_list:
            paths,file_name = os.path.split(str(paths2))
            paths = paths.split('\\')[-1]
            code_name = file_name.split('_')[0]
            if (paths1 == code_name) and (paths == "val"):
                shutil.copy(total_path/f'{paths}/{file_name}', dest_path/f'{paths}/{file_name}')
                i+=1
                if i>39:
                    i = 0
                    break
            elif (paths1 == code_name) and (paths == "train"):
                shutil.copy(total_path/f'{paths}/{file_name}', dest_path/f'{paths}/{file_name}')
                i+=1
                if i>159:
                    i = 0
                    break

@timeit
def test_create_label_files():
    label_info = pd.read_csv(args.data_path / 'db/annotations2.csv')
    label_info2 = pd.read_csv(args.data_path / 'db/label_list.csv')

    label_merge = pd.merge(label_info2, label_info, left_on = '0', right_on = 'file_name', how = 'inner')
    label_merge.drop(['0','id'],axis=1,inplace=True)
    label_merge.to_csv(args.data_path / 'db/final_label_list.csv', encoding = 'utf-8-sig', index=False)
    # label_dict = dict(zip(list(label_info2['id'].unique()), range(len(list(label_info2['id'].unique())))))
    
    # for index, row in label_info.iterrows():
    #     file_name = row['file_name'].split('.')[0]
    #     x, y, w, h = json.loads(row['bbox'])
    #     x, y, w, h = 0.5, 0.5, (w//2)/(w//2+pad*2), (h//2)/(h//2+pad*2)
    #     result = ' '.join(map(str, [label_dict[row['dl_mapping_code']], x, y, w, h]))
    #     with open(path / f'{file_name}.txt', 'w') as f:
    #         f.write(result)

@timeit
def split_label_image(): #폴더안의 파일 8:2 비율로 나눠주는 함수
    splitfolders.ratio(args.data_path/'train\\d',output = args.data_path/'train\\a',seed=1337,ratio=(.8,.2))
@timeit
def test_create_label_csv(): #250만개 전체의 라벨에서 95만개의 라벨과 교집합되는 데이터를 csv로 생성하는 함수
    label_info = pd.read_csv(args.data_path / 'db/label_list.csv')
    # label_info[['file_name', 'bbox', 'dl_mapping_code']].to_csv(args.data_path / 'db/annotations4.csv',encoding='utf-8-sig', index=False)
    label_info2 = pd.read_csv(args.data_path / 'db/annotations4.csv')

    label_merge = pd.merge(label_info, label_info2, left_on = '0', right_on = 'file_name', how = 'inner')
    label_merge.drop(['0','id'],axis=1,inplace=True)
    label_merge.to_csv(args.data_path / 'db/final_label_list.csv', encoding = 'utf-8-sig', index=False)

@timeit
def test_create_label_files(path, pad = args.im_padding):
    label_info = pd.read_csv(args.data_path / 'db/final_label_list.csv')
    label_dict = dict(zip(list(label_info['dl_mapping_code'].unique()), range(len(list(label_info['dl_mapping_code'].unique())))))
    path_list = path.rglob('*.png')
    for paths in path_list:
        save_path = str(paths).split('.')[0].split('K')[0]
        file_name = label_info[label_info['file_name']==str(paths).split('\\')[-1]]['file_name'].values[0].split('.')[0]
        x, y, w, h = json.loads(label_info[label_info['file_name']==str(paths).split('\\')[-1]]['bbox'].values[0])
        x, y, w, h = 0.5, 0.5, (w//2)/(w//2+pad*2), (h//2)/(h//2+pad*2)
        result = ' '.join(map(str, [label_dict[file_name.split('_')[0]], x, y, w, h]))
        with open(save_path + f'{file_name}.txt', 'w') as f:
            f.write(result)
@timeit
def remove_label(path): #하위폴더의 모든 txt확장자 파일 삭제
    path_list = path.rglob('*.txt')
    for paths in path_list:
        os.remove(str(paths))


@timeit
def test_warm(): #위험 조합 알약 데이터파일 교집합하여 추출하는 함수
    label_info = pd.read_csv(args.data_path / 'db/warm.csv')
    # label_info2 = pd.read_csv(args.data_path / 'db/final_label_list.csv')
    val_imglist = pd.read_csv(args.data_path / 'db/val_imglist.csv')
    match_warm = pd.read_csv(args.data_path / 'db/val_match_warm.csv')
    a = pd.merge(label_info,val_imglist,left_on='name',right_on='dl_mapping_code',how='inner')
    # a.to_csv(args.data_path / 'db/val_match_warm.csv',encoding='utf-8-sig')
    print(len(match_warm['name'].unique()))

@timeit
def test_val_imglabel_list(): # 
    label_info = pd.read_csv(args.data_path / 'db/final_label_list.csv')
    path = args.data_path/'train/final_data3/val'
    path_list = path.rglob('*.png')
    a=[]
    for paths in path_list:
        file_name = str(paths).split('\\')[-1]
        a.append(file_name)
    df = pd.DataFrame(a,columns=['name'])
    df = pd.merge(df,label_info,left_on='name',right_on='file_name',how='inner')
    df.drop(columns=['name'],inplace=True)
    df.to_csv(args.data_path/'db/val_imglist.csv',encoding='utf-8-sig')
def abc():
    total_path_list = args.data_path/'train/final_data3'
    total_list = total_path_list.rglob('*')
    i = 0
    for paths2 in total_list:
        paths,file_name = os.path.split(str(paths2))
        paths = paths.split('\\')[-1]
        # file_name = file_name.split('_')[0]
        print(file_name)
        break