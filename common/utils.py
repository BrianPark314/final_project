import zipfile
from functools import wraps
from common.params import args
import time
import orjson
import json
import os
import yaml
import pandas as pd
from pathlib import Path

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

@timeit
def create_yaml(path):
    with open(path/'data.yaml', 'w') as f:
        names = sorted(list(pd.read_csv(path / 'db/table.csv')['dl_mapping_code']))
        y = {'path': str(path), 
             'train': '../train/',
             'validation': '../validation/', 
             'test': '../test/',}
        yaml.dump(y, f)
        yaml.dump({'names':names}, f, default_flow_style=None)

@timeit
def create_dirs(path_list): 
    for paths in path_list:
        os.makedirs(paths /'data/db', exist_ok=True)
        # os.makedirs(paths /'images', exist_ok=True)
        # os.makedirs(paths /'labels', exist_ok=True) 

@timeit
def unzip(path):
    path_list = path.rglob('*.zip')
    for paths in (path_list):
        with zipfile.ZipFile(paths, 'r') as zip_ref:
            zip_ref.extractall(str(paths)[:-4])
            os.remove(zip_ref)

@timeit
def parse_json(path):
    path_list = path.rglob('*')
    frame = []
    annotations_frame=[]
    for paths in path_list:
        json_path = paths.glob('**/*.json')
        for j in json_path:
            with open(j,'rt', encoding='UTF-8') as json_file:
                pill_code = json.loads(json_file.read())['images'][0]
            with open(j,'rt', encoding='UTF-8') as json_file:
                annotations = json.loads(json_file.read())['annotations'][0]
            # break
            frame.append(pill_code)
            annotations_frame.append(annotations)
    # pd.DataFrame(frame).to_csv(args.data_path / 'db/table.csv')
    # pd.DataFrame(annotations_frame).to_csv(args.data_path / 'db/annotations.csv')
    df1 = pd.DataFrame(annotations_frame)
    df2 = pd.DataFrame(frame)
    result1 = pd.concat([df2,df1],axis=1)
    pd.DataFrame(result1).to_csv(args.data_path / 'db/annotations.csv')
@timeit
def move_image(path):
    path_list = path.rglob('*.png')
    for paths in path_list:
        file_name = str(paths).split('/')[-1]
        os.replace(str(paths), str(path)+f'/images/{file_name}')

@timeit
def create_label_files(path):
    path_list = path.rglob('*')
    i=0
    cnt = 0
    for paths in path_list:
        cnt += 1
        png_path_list = paths.glob('**/*.png')
        label_path = str(path / 'labels')
        textfile =pd.read_csv(args.data_path / 'db/annotations.csv')
        for paths2 in png_path_list:
            i += 1
            file_name = str(paths2).split('\\')[-1].split('.')[0]
            x,y,w,h = json.loads(textfile['bbox'][i-1])
            dot = [(cnt-1), ((x-((976-640)/2))+(w/2))/640, ((y-((1280-640)/2))+(h/2))/640, w/640, h/640] #좌표값 상대 좌표로 변환
            result = ' '.join(str(s) for s in dot)
            if textfile['file_name'][i-1].split('.')[0] == file_name:
                Path(label_path+f'/{file_name}.txt').write_text(result)
        # with open(label_path+f'/{file_name}.txt', 'w') as f:
        #     f.write('')