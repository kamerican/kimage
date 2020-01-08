from datetime import datetime
from time import time
import cv2
from kimage import constant


# Functions
def sort_function(picture):
    return picture.stat().st_ctime
def rename_images():
    # not sure if working
    picture_number = 0
    count = 0
    previous_datetime_string = ""
    picture_dir = constant.BASE_DIR / 'database' / 'rename'
    picture_list = list(picture_dir.glob('*'))
    sorted_list = sorted(picture_list, key=sort_function)
    for picture_path in sorted_list:
        created_datetime = datetime.fromtimestamp(picture_path.stat().st_ctime)
        created_datetime_string = created_datetime.strftime("%y%m%d_%H%M%S")

        if created_datetime_string == previous_datetime_string:
            count += 1
            if count > 999:
                previous_datetime_string = created_datetime_string
                raise Exception("Error: count exceeded 999 for {}".format(picture_path))
        else:
            # if count != 0:
            #     print(count)
            count = 0
        rename_string = "{0}_{1}{2}".format(
            created_datetime_string,
            str(count).zfill(3),
            picture_path.suffix,
        )
        previous_datetime_string = created_datetime_string
        rename_path = picture_dir / rename_string
        picture_number += 1
        # if picture_number % 500 == 0:
        #     print(picture_number)
        #     print(rename_path)
        if not rename_path.is_file():
            print("{0} -> {1}".format(
                picture_path.name,
                rename_path.name,
            ))
            picture_path.rename(rename_path)
def move_json():
    time_start = time()
    number_of_json = 0
    image_directory = constant.IMAGE_DIR
    for folder in image_directory.iterdir():
        # print(folder)
        for image in folder.glob('*.json'):
            target = constant.DUMP_DIR.joinpath(image.name)
            # print(image.name)
            # print(target)
            image.replace(target)
            number_of_json += 1
            # break
        # break
    print("Moved {0} json files in {1} seconds.".format(
        number_of_json,
        round(time() - time_start),
    ))


# Script section
move_json()
