import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from common.params import args
def creat_random_sample_img():
    img_path1=''
    img_path2=''
    img_path3=''
    img_path4=''
    warm_img_list=[]
    path = args.data_path/'train/final_data3/val'
    warm_list = pd.read_csv(args.data_path / 'db/merge_val_warm_list.csv')
    warm_list_unique = warm_list['warm_drug_N'].unique()
    paths_list = path.rglob('*.png')
    for _ in range(10):
        sample = np.random.choice(warm_list_unique, 4, replace=False)
        img_list=[]
        for list in sample:
            img_list.append(str(path) + '\\' + warm_list[warm_list['warm_drug_N'] == list].sample(n=1)['file_name'].values[0])
        img_path1,img_path2,img_path3,img_path4=img_list
        img1=cv2.imread(img_path1,1)
        img1=cv2.resize(img1,(200,200))
        img2=cv2.imread(img_path2,1)
        img2=cv2.resize(img2,(200,200))
        img3=cv2.imread(img_path3,1)
        img3=cv2.resize(img3,(200,200))
        img4=cv2.imread(img_path4,1)
        img4=cv2.resize(img4,(200,200))
        addh1=cv2.hconcat([img1,img2])
        addh2=cv2.hconcat([img3,img4])
        fin_img = cv2.vconcat([addh1,addh2])
        cv2.imwrite(f'{str(args.data_path)}\\sample\\sample{_}.png',fin_img)
        label = ' '.join(map(str,sample))
        with open(f'{str(args.data_path)}\\sample\\sample_label{_}.txt', 'w') as f:
            f.write(label)