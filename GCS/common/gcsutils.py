import sys
from pathlib import Path
import os
sys.path.insert(0, '/Users/Shark/Projects/final_project')
from common.params import args
from common.image import resize_image
import subprocess
from more_itertools import ichunked
import pandas as pd

# def organize_images(url_list_nested):
#     bucket = init_bucket()
#     for url in url_list_nested:
#         blob = bucket.blob(url + '*.png')
#         print(blob)

def organize_images(url_list_nested, target_path=args.gsutil_train_path):
    for url in url_list_nested:
        subprocess.run(['bash',str(args.script_path / 'move.sh'), url, target_path])

def resize(url_list_img):
    label_info = pd.read_csv(args.data_path / 'db/annotations.csv')
    chunked_list = ichunked(url_list_img, 1000)

    for url in chunked_list:
        os.makedirs(str(args.GCS_path / 'cache'), exist_ok=True)
        with open(args.GCS_path / 'logs/temp.txt', 'w') as f:
            f.write('\n'.join(url))
        subprocess.run(['bash', str(args.script_path / 'm_download_img.sh'),
                        " ".join(url), str(args.GCS_path / 'cache'),
                        str(args.GCS_path / 'logs')])
        resize_image(args.GCS_path / 'cache', label_info)
        subprocess.run(['bash', str(args.script_path / 'upload_img.sh'), str(args.GCS_path),
                        " ".join(url), args.gcs_processed_path,])




        