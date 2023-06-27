from common.params import args
from common.utils import create_dirs, unzip, parse_json, move_image

if __name__ == '__main__':
    train_path = args.data_path / 'train/'
    valid_path = args.data_path / 'validation'
    test_path = args.data_path / 'test/'
    #create_dirs([train_path, valid_path, test_path])
    #unzip(train_path)
    #parse_json(train_path)
    move_image(train_path)