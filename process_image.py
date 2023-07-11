from common.image import resize_image
from common.utils import args

if __name__ == '__main__':
    resize_image(args.data_path / 'validation', args.im_size)
