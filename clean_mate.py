import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description="清除图片头信息，减小图片体积")
parser.add_argument('--path', type=str, default='./', help='清理目录，默认当前目录')
sys_args = parser.parse_args()

def get_files():
    for root, dirs, files in os.walk(sys_args.path):
        for file in files:
            if '.png' in file: yield os.path.join(root, file)

def del_mate(f_path):
	img = Image.open(f_path)
	img.save(f_path) 


if __name__ == '__main__':
	for file in get_files():
		del_mate(file)
