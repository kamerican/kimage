from pathlib import Path
import argparse
from kimage.downloader import Downloader
from kimage.manager import Manager
from kimage import constant

def download_images_from_urls_txt():
    downloader = Downloader()
    urls = Path('urls.txt')
    with urls.open(mode='r', newline='') as f:
        url_list = f.readlines()
    # print(url_list)
    downloader.download_from_list_of_urls(url_list)
def update_picture_database():
    session = constant.session_factory()
    manager = Manager()
    has_new_pictures = manager.update_db_images(session)
    if has_new_pictures:
        print("Committing database additions")
        session.commit()
def rename_images_in_rename_dir():
    manager = Manager()
    manager.rename_images()


parser = argparse.ArgumentParser(description='Execute different processes.')
parser.add_argument(
    'case',
    type=int,
    help='Integer representing the process to be executed',
)
args = parser.parse_args()
if args.case == 0:
    download_images_from_urls_txt()
elif args.case == 1:
    update_picture_database()
elif args.case == 2:
    rename_images_in_rename_dir()
else:
    print("Unknown case number: {}".format(args.case))
