from common.params import args
import zipfile
from functools import wraps
import time
from glob import glob, iglob
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
def create_dirs(train_path, valid_path, test_path):
    os.makedirs(train_path /'images', exist_ok=True)
    os.makedirs(train_path /'labels', exist_ok=True) 
    os.makedirs(valid_path /'images', exist_ok=True) 
    os.makedirs(valid_path /'labels', exist_ok=True) 
    os.makedirs(test_path /'images', exist_ok=True) 
    os.makedirs(test_path /'labels', exist_ok=True) 


@timeit
def unzip(path):
    path_list = glob(str(path) +  '/*/*/*.zip', recursive=True)
    for paths in (path_list):
        with zipfile.ZipFile(paths, 'r') as zip_ref:
            zip_ref.extractall(paths[:-4])
            os.remove(zip_ref)

@timeit
def parse_json(path):
    path_list = iglob(str(path)+ '/*.json', recursive=True)
    for paths in path_list:
        print(paths)

