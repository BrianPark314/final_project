from common.params import args
from common.utils import create_dirs, unzip, parse_json, move_image, create_label_files, create_yaml
from common.image import get_contour, resize_image
import time
import os
from pathlib import Path

if __name__ == '__main__':
    train_path = args.data_path / 'train/'
    valid_path = args.data_path / 'validation/'
    test_path = args.data_path / 'test/'

    # create_dirs(args.data_path, [train_path, valid_path, test_path])
    # unzip(args.down_path, args.data_path)
    # parse_json(args.data_path)
    # create_yaml(args.data_path)
    # create_label_files(train_path / 'labels')
    while(True):
        try:
            unzip(args.down_path,train_path /'images/')
            move_image(args.data_path / 'unzip/', train_path)
            resize_image(train_path / 'images/')
            # get_contour(train_path / 'images/')
        except:
            print("not complete unzip")
        time.sleep(60)

    # split_label_image(train_path)
    # create_dirs(args.data_path, [train_path, valid_path, test_path])
    # unzip(args.data_path, args.data_path / 'unzip')
    # unzip(args.down_path, args.data_path / 'unzip')
    # parse_json(args.data_path)
    # move_image(args.data_path / 'unzip/', train_path)
    # resize_image(train_path / 'images/')
    # create_yaml(args.data_path)
    # create_label_files(args.data_path / 'processed')
    # get_contour(train_path / 'images/')


