from pathlib import Path
from uuid import uuid4
import itertools
import cv2
from sqlalchemy.orm.exc import MultipleResultsFound
from kimage.models import Picture
from kimage import constant

class Manager():
    """
    Class controlling images in linked to the database.
    """
    def __init__(self, resize_factor=0.25, blocking=True):
        database_dir = Path(__file__).parent / 'database'
        self.blocking = blocking
        self.image_extension_list = ['jpg', 'png']
        self.resize_factor = resize_factor
        self.picture_dir = database_dir / 'picture'
        self.face_dir = database_dir / 'face'
        self.original_dir = database_dir / 'original'
        self.rename_dir = database_dir / 'rename'
        self.download_dir = database_dir / 'download'
        self.delete_dir = database_dir / 'delete'
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
    def refresh_all_db_images(self, session):
        """
        Checks all images in picture dir if in the database.
        If not, adds image to the database.
        Takes a long time because of the number of images.
        """
        has_new_pictures = False
        picture_path_chain = self.get_image_glob(self.picture_dir)
        i_picture = 0
        for picture_path in picture_path_chain:
            i_picture += 1
            if i_picture % 1000 == 0:
                print("Picture #{}".format(i_picture))
            try:
                # Check if there are duplicate filenames already in db
                picture_match = (
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
                if picture_match:
                    # Current picture already in db
                    # print("Already in database:", picture_path.name)
                    pass
                else:
                    # Add picture to db
                    has_new_pictures = True
                    print("Adding to database:", picture_path.name)
                    picture = Picture()
                    picture.filename = picture_path.name
                    session.add(picture)
        return has_new_pictures
    def add_new_images_to_db(self, session, source_dir):
        """
        Checks if images in a given directory are already in the database.
        If not, then add image to picture table and move image into picture directory.
        """
        has_new_pictures = False
        picture_path_chain = self.get_image_glob(source_dir)
        for picture_path in picture_path_chain:
            # Check if there are duplicate filenames already in db
            picture_match = (
                session.query(Picture)
                .filter_by(filename=picture_path.name)
                .one_or_none()
            )
            if not picture_match:
                # Add picture to db
                has_new_pictures = True
                print("Adding to database:", picture_path.name)
                picture = Picture()
                picture.filename = picture_path.name
                session.add(picture)
                new_path = self.picture_dir / picture_path.name
                picture_path.rename(new_path)
        return has_new_pictures
    def rename_images(self):
        """
        Renames images in the rename directory to a random 19-char string.
        """
        to_rename_path_chain = self.get_image_glob(self.rename_dir)
        for to_rename_path in to_rename_path_chain:
            # if len(rename_path.name) != constant.PICTURE_FILE_STRING_LENGTH:
            for i_try in range(1, 5):
                new_name = "{0}{1}".format(
                    uuid4().hex[:constant.PICTURE_NAME_STRING_LENGTH],
                    to_rename_path.suffix,
                )
                new_path = self.rename_dir / new_name
                if not new_path.is_file():
                    to_rename_path.rename(new_path)
                    break
            else:
                print("Could not get a unique filename in {} tries...".format(i_try))
    def get_image_dimensions(self, session):
        """
        Save image dimensions to the database.
        """
        has_updated_dimensions = False
        picture_match = (
            session.query(Picture)
            .filter_by(height=None)
        )
        if picture_match:
            has_updated_dimensions = True
            for picture in picture_match:
                image = cv2.imread(str(picture.filepath))
                picture.height = image.shape[0]
                picture.width = image.shape[1]
                self._show_image(image, picture.filename)
            # cv2.destroyAllWindows()
        return has_updated_dimensions
    def resize_images(self, session):
        """
        Resize images whose size is greater than a threshold.
        """
        has_resized_images = False
        size_limit = 2048**2
        picture_match = (
            session.query(Picture)
            .filter_by(is_resized=False)
        )
        if picture_match:
            for picture in picture_match:
                picture_size = picture.height * picture.width
                if picture_size > size_limit:
                    has_resized_images = True
                    dim = (
                        picture.width * self.resize_factor,
                        picture.height * self.resize_factor,
                    )
                    image = cv2.imread(str(picture.filepath))
                    resize_path = str(picture.filepath)
                    resized_image = cv2.resize(image, dim)
                    # Move original image to original dir
                    original_path = self.original_dir / picture.filename
                    picture.filepath.rename(original_path)
                    picture.is_resized = True
                    cv2.imwrite(resize_path, resized_image)
        return has_resized_images
    def delete_images_from_db(self, session):
        """
        Gets images in the delete directory.
        Deletes those same images from the db and picture directory.
        """
        # count = 0
        has_deleted_images = False
        picture_path_chain = self.get_image_glob(self.delete_dir)
        for picture_path in picture_path_chain:
            picture_match = (
                session.query(Picture)
                .filter_by(filename=picture_path.name)
                .one_or_none()
            )
            if picture_match and picture_match.filepath.is_file():
                has_deleted_images = True                
                # count += 1
                # print(picture_match.filepath)
                print("Deleting from database and picture directory:", picture_match.filename)
                picture_match.filepath.unlink()
                session.delete(picture_match)
        # print(count)
        return has_deleted_images
    ### Private
    def _show_image(self, image, filename):
        cv2.imshow(filename, image)
        if self.blocking:
            cv2.waitKey(0)
