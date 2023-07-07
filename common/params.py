import easydict
from pathlib import Path
import os

args = easydict.EasyDict()
args.base_path = Path(os.getcwd())
args.data_path = Path('/content/data')
args.script_path = args.base_path / 'GCS/scripts/'
