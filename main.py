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
    has_new_pictures = manager.refresh_all_db_images(session)
    if has_new_pictures:
        print("Committing database additions")
        session.commit()
def rename_images_in_rename_dir():
    manager = Manager()
    manager.rename_images()
def add_images_from_download_and_rename_to_database_and_picture_dir():
    session = constant.session_factory()
    manager = Manager()
    # Add images from rename dir
    manager.rename_images()
    has_new_rename_images = manager.add_new_images_to_db(
        session=session,
        source_dir=manager.rename_dir,
    )
    # Add images from download dir
    has_new_download_images = manager.add_new_images_to_db(
        session=session,
        source_dir=manager.download_dir,
    )
    if has_new_rename_images or has_new_download_images:
        print("Committing database additions")
        session.commit()
def delete_selected_images():
    session = constant.session_factory()
    manager = Manager()
    has_deleted_images = manager.delete_images_from_db(session)
    if has_deleted_images:
        print("Committing database deletions")
        session.commit()

parser = argparse.ArgumentParser(description='Execute different processes.')
parser.add_argument(
    'case',
    type=int,
    help='Integer representing the process to be executed',
)
args = parser.parse_args()
if args.case == 0:
    download_images_from_urls_txt()
elif args.case == 99:
    update_picture_database()
elif args.case == 2:
    rename_images_in_rename_dir()
elif args.case == 1:
    add_images_from_download_and_rename_to_database_and_picture_dir()
elif args.case == 3:
    delete_selected_images()
else:
    print("Unknown case number: {}".format(args.case))
