from pathlib import Path
import argparse
from sqlalchemy.orm.exc import MultipleResultsFound
from kimage.downloader import Downloader
from kimage.manager import Manager
from kimage.models import Picture
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
    has_new_pictures = False

    picture_path_chain = manager.get_image_glob(manager.picture_dir)

    for picture_path in picture_path_chain:
        # print("Processing:", picture_path.name)
        try:
            # Check if there are duplicate filenames already in db
            picture_match_list = (
                session.query(Picture)
                .filter_by(filepath=picture_path.name)
                .one_or_none()
            )
        except MultipleResultsFound as error:
            # There's an picture with the same filename in db
            print("Error:", error)
            print("Multiple pictures found in database with the same filename:", picture_path.name)
        else:
            # One or no pictures with same filename have been found in db
            if picture_match_list:
                # Current picture already in db
                print("Already in database:", picture_path.name)
            else:
                # Add picture to db
                has_new_pictures = True
                print("Adding to database:", picture_path.name)
                picture = Picture()
                picture.filepath = picture_path
                session.add(picture)
    if has_new_pictures:
        print("Committing database additions")
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
elif args.case == 1:
    update_picture_database()
else:
    print("Unknown case number: {}".format(args.case))
