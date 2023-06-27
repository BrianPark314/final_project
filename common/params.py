import easydict
from pathlib import Path
import os

args = easydict.EasyDict()
args.base_path = Path(os.getcwd())
args.data_path = args.base_path / 'data/'
