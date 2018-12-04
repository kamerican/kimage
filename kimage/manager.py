from pathlib import Path
import itertools
import cv2
from sqlalchemy.orm.exc import MultipleResultsFound
from kimage.models import Picture

class Manager():
    """
    Class controlling images in linked to the database.
    """
    def __init__(self, resize_factor=0.25):
        self.image_extension_list = ['jpg', 'png']
        self.resize_factor = resize_factor
        database_dir = Path(__file__).parent / 'database'
        self.picture_dir = database_dir / 'picture'
        self.face_dir = database_dir / 'face'
        self.original_dir = database_dir / 'original'

    ### Public methods
    def get_image_glob(self, dir_path):
        """
        Returns a generator of images in a given image directory.
        """
        glob_gen_list = []
        for image_extension in self.image_extension_list:
            pattern = '*.' + image_extension
            glob_gen = dir_path.glob(pattern)
            glob_gen_list.append(glob_gen)
        return itertools.chain.from_iterable(glob_gen_list)
    def update_db_images(self, session):
        has_new_pictures = False
        picture_path_chain = self.get_image_glob(self.picture_dir)
        i_picture = 0
        for picture_path in picture_path_chain:
            i_picture += 1
            print("Picture #{}".format(i_picture))
            if i_picture % 1000 == 0:
                print("Picture #{}".format(i_picture))
            if i_picture > 40:
                break
            try:
                # Check if there are duplicate filenames already in db
                picture_match_list = (
                    session.query(Picture)
                    .filter_by(filename=picture_path.name)
                    .one_or_none()
                )
            except MultipleResultsFound as error:
                # There's an picture with the same filename in db
                print("Error:", error)
                print("Multiple pictures in database with the same filename:", picture_path.name)
            else:
                # One or no pictures with same filename have been found in db
                if picture_match_list:
                    # Current picture already in db
                    # print("Already in database:", picture_path.name)
                    pass
                else:
                    # Add picture to db
                    has_new_pictures = True
                    image = cv2.imread(str(picture_path))
                    #print("Adding to database:", picture_path.name)
                    picture = Picture()
                    picture.filename = picture_path.name
                    picture.height = image.shape[0]
                    picture.width = image.shape[1]
                    session.add(picture)
                    cv2.imshow('Preview', image)
                    cv2.waitKey(0)
        cv2.destroyAllWindows()
        return has_new_pictures

# # Get resized image and save
# resized_image = cv2.resize(original_image, dim)
# resized_image_path = self.resize_dir_path / "rsz_{}".format(image_path.name)
# if resized_image_path.is_file():
#     print("Resized image already exists:", resized_image_path.name)
# else:
#     cv2.imwrite(str(resized_image_path), resized_image)
            

    ### Private
