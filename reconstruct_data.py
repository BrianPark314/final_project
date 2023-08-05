from common.params import args
from common.utils import create_dirs, unzip, parse_json, move_image, create_label_files, create_yaml
from common.model_improve_process import test_val_imglabel_list,split_label_image,image_path_move,label_path_move,train_image_label_redivide,test_create_label_files,remove_label,test_warm
from common.image import get_contour, resize_image
from common.create_sample_img import creat_random_sample_img
import time
import os
import subprocess
from pathlib import Path

if __name__ == '__main__':
    train_path = args.data_path / 'train/'
    valid_path = args.data_path / 'validation/'
    test_path = args.data_path / 'test/'
    div_path = args.data_path / 'processed/'
    # create_dirs(args.data_path, [train_path, valid_path, test_path])
    # unzip(args.down_path, args.data_path)
    # parse_json(args.data_path)
    # create_yaml(args.data_path)
    # create_label_files(train_path / 'labels7')
    # remove_label(train_path/'final_data2')
    # test_create_label_files(train_path / 'final_data2')
    # test_create_label_files()
    # image_path_move()
    # label_path_move()
    # test_warm()
    # test_val_imglabel_list()
    creat_random_sample_img()
    # train_image_label_redivide()
    # while(True):
    #     try:
    #         subprocess.run([str(args.script_path / 'unzip_test.sh'),str(train_path /'unzip/'),str(train_path /'processed/')],shell=True)
    #         move_image(train_path /'unzip/', train_path /'processed/')
    #         resize_image(train_path /'processed/')
    #         move_image(train_path /'processed/', train_path /'images/')
    #         # get_contour(train_path / 'images/')
    #         if len(os.listdir('C:/Users/user/Downloads/166.약품식별 인공지능 개발을 위한 경구약제 이미지 데이터/01.데이터/2.Validation/원천데이터/단일경구약제 5000종')) ==0:
    #             break
    #     except:
    #         print("not complete unzip")
    #     time.sleep(60)
    # create_label_files(args.data_path / 'processed')
    # split_label_image()
    # create_dirs(args.data_path, [train_path, valid_path, test_path])
    # unzip(args.data_path, args.data_path / 'unzip')
    # unzip(args.down_path, args.data_path / 'unzip')
    # parse_json(args.data_path)
    # move_image(args.data_path / 'unzip/', train_path)
    # resize_image(train_path / 'images/')
    # create_yaml(args.data_path)
    # create_label_files(args.data_path / 'processed')
    # get_contour(train_path / 'images/')