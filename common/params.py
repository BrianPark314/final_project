import easydict
from pathlib import Path
import os

args = easydict.EasyDict()
args.base_path = Path(os.getcwd())
args.data_path = Path(args.base_path/'data')

args.im_size = 320
args.im_padding = 20