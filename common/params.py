import easydict
from pathlib import Path
import os

args = easydict.EasyDict()
args.base_path = Path(os.getcwd())
args.data_path = Path(args.base_path/'data')
args.down_path = Path('C:/Users/user/Downloads/166.약품식별 인공지능 개발을 위한 경구약제 이미지 데이터/01.데이터/2.Validation')
args.path_to_unzip = Path('C:/Users/user/Downloads/unzipfile')
args.script_path = Path('C:/python/finalproject/final_project_2/GCS/scripts')

args.im_size = 320
args.im_padding = 20