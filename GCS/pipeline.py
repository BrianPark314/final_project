import subprocess
import sys
import os
sys.path.insert(0, os.getcwd())
import time

from common.params import args

if __name__ == '__main__':
    while(True):
        try:
            subprocess.run(args.script_path / 'unzip.sh')
        except:
            print('No zip file download complete.')
        subprocess.run(args.script_path / 'upload.sh')
        subprocess.run(args.script_path / 'clean.sh')  
        time.sleep(60)      
    # subprocess.run(args.script_path / 'test.sh')
    # print(os.environ['file'])