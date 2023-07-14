from common.image import resize_image, multiprocess
from common.utils import args
import splitfolders

if __name__ == '__main__':
    #resize_image(args.data_path / 'validation', args.im_size)
    multiprocess(args.data_path / 'validation')
    