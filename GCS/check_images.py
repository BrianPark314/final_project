import sys
import os
sys.path.insert(0, os.getcwd())
from common.gcsutils import check_images

if __name__ == '__main__':
    check_images()