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
import gc
from glob import glob


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
        names = sorted(list(pd.read_csv(path / 'db/annotations.csv')['dl_mapping_code'].unique()))
        y = {'path': str(path), 
             'train': '../train/',
             'validation': '../validation/', 
             'test': '../test/',
             'nc':len(names)}
        yaml.dump(y, f)
        yaml.dump({'names':names}, f, default_flow_style=None)

@timeit
def create_dirs(data_path, path_list):
    os.makedirs(data_path /'db', exist_ok=True)
    for paths in path_list:
        os.makedirs(paths /'data/db', exist_ok=True)
        # os.makedirs(paths /'images', exist_ok=True)
        # os.makedirs(paths /'labels', exist_ok=True) 

@timeit
def unzip(zip_path, unzip_path):
    os.makedirs(unzip_path, exist_ok=True)
    path_list = zip_path.rglob('*.zip')
    for paths in (path_list):
        with zipfile.ZipFile(paths, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            os.remove(str(paths))

@timeit
def parse_json(path):
    code_list = []
    annotations_list = []
    json_path = path.rglob('*.json')
    for j in json_path:
        with open(j,'rt', encoding='UTF-8') as json_file:
            json_read = orjson.loads(json_file.read())
            pill_code = json_read['images'][0]
            annotations = json_read['annotations'][0]
        code_list.append(pill_code)
        annotations_list.append(annotations)

    result = pd.concat([pd.DataFrame(annotations_list),pd.DataFrame(code_list)],axis=1).sort_values(by='file_name')
    result[['file_name', 'bbox', 'dl_mapping_code']].to_csv(args.data_path / 'db/annotations.csv',encoding='utf-8-sig', index=False)

@timeit
def move_image(ori_path, move_path):
    path_list = ori_path.rglob('*.png')
    for paths in path_list:
        #file_name = str(paths).split('/')[-1]
        _, file_name = os.path.split(paths)
        os.replace(str(paths), str(move_path)+f'/images/{file_name}')

@timeit
def create_label_files(path, pad = args.im_padding):
    label_info = pd.read_csv(args.data_path / 'db/annotations.csv')
    label_dict = dict(zip(list(label_info['dl_mapping_code'].unique()), range(len(list(label_info['dl_mapping_code'].unique())))))

    for index, row in label_info.iterrows():
        file_name = row['file_name'].split('.')[0]
        x, y, w, h = json.loads(row['bbox'])
        x, y, w, h = 0.5, 0.5, (w//2)/(w//2+pad*2), (h//2)/(h//2+pad*2)
        result = ' '.join(map(str, [label_dict[row['dl_mapping_code']], x, y, w, h]))
        with open(path / f'{file_name}.txt', 'w') as f:
            f.write(result)
