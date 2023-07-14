import easydict
from pathlib import Path
import os

args = easydict.EasyDict()
args.base_path = Path(os.getcwd())
args.data_path = Path(args.base_path/'data')
args.script_path  = args.base_path / 'GCS/scripts'

args.im_size = 320
args.im_padding = 20

args.bucket_name = 'pill_data_brain'
args.gsutil_train_path = 'gs://pill_data_brain/train/images'
args.GCS_path = args.base_path / 'GCS'