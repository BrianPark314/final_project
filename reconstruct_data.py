from common.params import args
from common.utils import create_dirs, unzip, parse_json, move_image, create_label_files, create_yaml
from common.image import get_contour, resize_image
import argparse
from pathlib import Path
if __name__ == '__main__':
    FUNCTION_MAP = {'create_dirs' : create_dirs,
                 'unzip' : unzip,
                 'parse_json' : parse_json,
                 'move_image' : move_image,
                 'create_label_files' : create_label_files,
                 'create_yaml' : create_yaml,
                 'get_contour' : get_contour,
                 'resize_image' : resize_image, }

    parser = argparse.ArgumentParser()
    parser.add_argument('--command', choices=FUNCTION_MAP.keys(), help = 'choose the function to run.')
    parser.add_argument('--path', default='choose the data path.')
    opt = parser.parse_args()

    file_path = args.data_path / Path(opt.path)

    func = FUNCTION_MAP['opt.command']
    func()


