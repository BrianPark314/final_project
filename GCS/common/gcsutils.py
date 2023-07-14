from google.cloud import storage
import sys
from pathlib import Path
import os
sys.path.insert(0, '/Users/Shark/Projects/final_project')
from common.params import args
from common.image import resize_image
import subprocess
from more_itertools import chunked
import pandas as pd

def init_bucket():
    client = storage.Client()
    bucket = client.get_bucket(args.bucket_name)
    return bucket

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
    gcs_original_path = "gs://pill_data_brain/train/images/"
    gcs_processed_path = "gs://pill_data_brain/processed/train"
    for url in url_list_img:
        os.makedirs(str(args.GCS_path / 'cache'), exist_ok=True)
        subprocess.run(['bash', str(args.script_path / 'download_img.sh'),gcs_original_path+url, str(args.GCS_path / 'cache')])
        resize_image(args.GCS_path / 'cache', label_info)
        subprocess.run(['bash', str(args.script_path / 'upload_img.sh'), str(args.GCS_path / 'cache'), gcs_processed_path])




        