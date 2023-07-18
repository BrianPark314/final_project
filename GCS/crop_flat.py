import sys
import subprocess
from common.gcsutils import organize_images, resize
import os
sys.path.insert(0, os.getcwd())

from common.params import args

if __name__ == '__main__':
    #subprocess.run(['bash', args.script_path / 'get_list.sh', str(args.GCS_path / 'logs')])
    with open(args.base_path / 'GCS/logs/log.txt', 'r') as f:
        url_list = sorted(f.read().splitlines())
    
    subprocess.run(['bash', args.script_path / 'get_complete_list.sh', str(args.GCS_path / 'logs')])

    with open(args.base_path / 'GCS/logs/complete.txt', 'r') as f:
        complete_list = sorted(f.read().splitlines())
    print('processed img files: ', len(complete_list))

    url_list_nested = sorted([_ for _ in url_list if _[-1] == '/'])
    url_list_nested = url_list_nested[3:]
    url_list_img = sorted([_ for _ in url_list if _.split('.')[-1] == 'png'])

    complete_list = [args.gcs_original_path+_.split('/')[-1] for _ in complete_list]
    url_list_truncated = sorted(list(set(url_list_img)-set(complete_list)))
    print ('total:', len(set(url_list_img)), 'remaining:', len(url_list_truncated))
    #organize_images(url_list_nested)
    resize(url_list_truncated)
    
