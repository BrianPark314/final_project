from common.params import args
import zipfile
from functools import wraps
import time
from glob import glob

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

@timeit
def unzip(path):
    extract_path = glob(str(path) +  '/**', recursive=True)
    print(extract_path)
    path_list = extract_path.glob('/*.zip')
    for paths in path_list:
        with zipfile.ZipFile(paths, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
