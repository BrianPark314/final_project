import zipfile
from functools import wraps
from common.params import args
import time
import orjson
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
        os.makedirs(paths /'images', exist_ok=True)
        os.makedirs(paths /'labels', exist_ok=True) 

@timeit
def unzip(path):
    path_list = path.rglob('*.zip')
    for paths in (path_list):
        with zipfile.ZipFile(paths, 'r') as zip_ref:
            zip_ref.extractall(str(paths)[:-4])
            os.remove(zip_ref)

@timeit
def parse_json(path):
    path_list = path.rglob('라벨링데이터/*/*/*')
    frame = []
    for paths in path_list:
        json_path = paths.glob('*.json')
        for j in json_path:
            with open(j) as json_file:
                pill_code = orjson.loads(json_file.read())['images'][0]

            break
        frame.append(pill_code)
    pd.DataFrame(frame).to_csv(args.data_path / 'db/table.csv')

@timeit
def move_image(path):
    path_list = path.rglob('*.png')
    for paths in path_list:
        file_name = str(paths).split('/')[-1]
        os.replace(str(paths), str(path)+f'/images/{file_name}')

@timeit
def create_label_files(path):
    label_path = str(path / 'labels')
    path_list = path.rglob('*.png')
    for paths in path_list:
        file_name = str(paths).split('/')[-1].split('.')[0]
        Path(label_path+f'/{file_name}.txt').write_text('')
        # with open(label_path+f'/{file_name}.txt', 'w') as f:
        #     f.write('')



