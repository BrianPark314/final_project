from common.params import args
from common.utils import unzip

if __name__ == '__main__':
    train_path = args.data_path / 'train/'
    valid_path = args.data_path / 'validation'
    test_path = args.data_path / 'test/'
    unzip(train_path)