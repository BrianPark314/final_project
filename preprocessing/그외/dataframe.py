import zipfile
from glob import glob, iglob
import os
import json
import pathlib
path = pathlib.Path('C:/Users/User/OneDrive - jbnu.ac.kr/문서/final_project/image data/01.데이터/1.Training/라벨링데이터/단일경구약제 5000종')

def unzip(path):
    path_list = path.rglob('*.zip')
    for paths in (path_list):
        with zipfile.ZipFile(paths, 'r') as zip_ref:
            zip_ref.extractall(str(paths)[:-4])
            # os.remove(str(zip_ref))