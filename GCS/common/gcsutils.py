import sys
from pathlib import Path
import os
sys.path.insert(0, os.getcwd())
from common.params import args
from common.image import resize_image
from common.utils import timeit
import subprocess
from more_itertools import ichunked
import pandas as pd
import shutil
from iteration_utilities import duplicates

# def organize_images(url_list_nested):
#     bucket = init_bucket()
#     for url in url_list_nested:
#         blob = bucket.blob(url + '*.png')
#         print(blob)

def set_cache():
    os.makedirs(str(args.GCS_path / 'cache'), exist_ok=True)
    shutil.rmtree(str(args.GCS_path / 'cache'))
    os.makedirs(str(args.GCS_path / 'cache'), exist_ok=True)


def organize_images(url_list_nested, target_path=args.gsutil_train_path):
    for url in url_list_nested:
        subprocess.run(['bash',str(args.script_path / 'move.sh'), url, target_path])

def resize(url_list_img):
    label_info = pd.read_csv(args.data_path / 'db/annotations.csv')
    chunked_list = ichunked(url_list_img, 1000)
    set_cache()

    for url in chunked_list:
        with open(args.GCS_path / 'logs/temp.txt', 'w') as f:
            f.write('\n'.join(url))
        subprocess.run(['bash', str(args.script_path / 'm_download_img.sh'),
                        " ".join(url), str(args.GCS_path / 'cache'),
                        str(args.GCS_path / 'logs')])
        resize_image(args.GCS_path / 'cache', label_info)
        subprocess.run(['bash', str(args.script_path / 'upload_img.sh'), str(args.GCS_path),
                        " ".join(url), args.gcs_processed_path,])
        
def resize_folder(folder_list):
    label_info = pd.read_csv(args.data_path / 'db/annotations.csv')
    set_cache()

    for folder in folder_list:
        try:
            subprocess.run(['bash', str(args.script_path / 'm_download_folder.sh'),
                            folder, str(args.GCS_path / 'cache'),
                            str(args.GCS_path / 'logs')])
            resize_image(args.GCS_path / 'cache', label_info)
            subprocess.run(['bash', str(args.script_path / 'upload_img.sh'), str(args.GCS_path),
                            folder, args.gcs_processed_path,])
            with open(args.base_path / 'GCS/logs/complete_folders.txt', 'a') as f:
                f.writelines(folder + '\n')
        except:
            with open(args.base_path / 'GCS/logs/complete_folders.txt', 'a') as f:
                f.write(folder + '\n')
            continue

def get_files_list(type):
    subprocess.run(['bash', args.script_path / f'get_{type}_list.sh',str(args.GCS_path / 'logs')])
    with open(str(args.GCS_path / f'logs/{type}.txt'), 'r') as f:
        type_list = f.read().split('\n')
    type_list = [_.split('/')[-1] for _ in type_list]
    return type_list

def get_difference_from_list(original, compared):
    for _ in [original, compared]:
        if len(set(_)) != len(_):
            print(f'list has {len(_)-len(set(_))} duplicates!', )
            return None
    

@timeit
def check_images():
    label_info = pd.read_csv(args.data_path / 'db/annotations.csv')
    total_list = label_info['file_name'].values.tolist()
    subprocess.run(['bash', args.script_path / 'get_processed_list.sh',str(args.GCS_path / 'logs')])
    with open(str(args.GCS_path / 'logs/processed.txt'), 'r') as f:
        processed_list = f.read().split('\n')
    processed_list = sorted([_.split('/')[-1] for _ in processed_list])
    subprocess.run(['bash', args.script_path / 'get_uploaded_list.sh',str(args.GCS_path / 'logs')])
    with open(str(args.GCS_path / 'logs/uploaded.txt'), 'r') as f:
        uploaded_list = f.read().split('\n')
    uploaded_list = list(set(sorted([_.split('/')[-1] for _ in uploaded_list])))
    print('total image count: ', len(total_list))
    print('uploaded image count: ', len(uploaded_list), round(len(uploaded_list)/len(total_list)*100, 0), '%')
    get_difference_from_list(total_list, uploaded_list)
    print('cropped image count: ', len(processed_list), round(len(processed_list)/len(total_list)*100, 0), '%')
    get_difference_from_list(uploaded_list, processed_list)




        