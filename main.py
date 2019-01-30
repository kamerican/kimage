from pathlib import Path
import argparse
from kimage.downloader import Downloader

parser = argparse.ArgumentParser(description='Execute different processes.')
parser.add_argument(
    'case',
    type=int,
    help='Integer representing the process to be executed',
)
args = parser.parse_args()
if args.case == 0:
    downloader = Downloader()
    urls = Path('urls.txt')
    with urls.open(mode='r', newline='') as f:
        url_list = f.readlines()
    # print(url_list)
    downloader.download_from_list_of_urls(url_list)
elif args.case == 1:
    pass
elif args.case == 2:
    pass
elif args.case == 3:
    pass
else:
    print("Unknown case number: {}".format(args.case))
