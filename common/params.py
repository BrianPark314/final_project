import easydict
from pathlib import Path
import os

args = easydict.EasyDict()
#args.base_path = Path(os.getcwd())
args.base_path = Path('/Volumes/ADATA HV320/data/166.약품식별 인공지능 개발을 위한 경구약제 이미지 데이터/01.데이터')
args.data_path = args.base_path / 'data/'
