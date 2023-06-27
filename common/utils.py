from common.params import args
import zipfile
from functools import wraps
import time
from glob import glob
from tqdm.auto import tqdm
import orjson
import os

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
    for paths in path_list:
        json_path = paths.glob('*.json')
        for j in json_path:
            with open(j) as json_file:
                json = orjson.loads(json_file.read())
                pill_code = json['images'][0]['drug_N'][3:]

            break

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
        with open(label_path+f'/{file_name}.txt', 'w') as f:
            f.write('')



