import sys
import subprocess
from common.gcsutils import organize_images, resize
sys.path.insert(0, '/Users/Shark/Projects/final_project')

from common.params import args

if __name__ == '__main__':
    subprocess.run(['bash', args.script_path / 'get_list.sh', str(args.GCS_path / 'logs')])
    with open(args.base_path / 'GCS/logs/log.txt', 'r') as f:
        url_list = sorted(f.read().splitlines()[1:])
    with open(args.base_path / 'GCS/logs/complete.txt', 'r') as f:
        complete_list = sorted(f.read().splitlines())
    print('completed img files: ', len(complete_list))

    url_list_nested = sorted([_ for _ in url_list if _[-1] == '/'])
    url_list_img = sorted([_.split('/')[-1] for _ in url_list if _.split('.')[-1] == 'png'])
    url_list_truncated = sorted(list(set(url_list_img)-set(complete_list)))

    #organize_images(url_list_nested)
    resize(url_list_truncated)

