import sys
import subprocess
from common.gcsutils import resize_folder
import os
sys.path.insert(0, os.getcwd())

from common.params import args

if __name__ == '__main__':
    #subprocess.run(['bash', args.script_path / 'get_list.sh', str(args.GCS_path / 'logs')])
    with open(args.base_path / 'GCS/logs/log.txt', 'r') as f:
        url_list = sorted(f.read().splitlines())
    
    with open(args.base_path / 'GCS/logs/complete_folders.txt', 'r') as f:
        complete_folder_list = sorted(f.read().splitlines())
    print('processed folders: ', len(complete_folder_list))

    url_list_nested = sorted([_ for _ in url_list if _[-1] == '/'])
    url_list_nested = url_list_nested[1:]
    
    url_list_nested_truncated = sorted(list(set(url_list_nested)-set(complete_folder_list)))
    print ('total:', len(set(url_list_nested)), 'remaining:', len(url_list_nested_truncated))
    resize_folder(url_list_nested_truncated)
    
