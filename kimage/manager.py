from pathlib import Path
import itertools
# import cv2


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

    # def resize_images(self, images_to_resize_query_list):
    #     for image_to_resize in images_to_resize_query_list:
    #         # Get original image from image path
    #         image_path = image_to_resize.filepath_original


    #         original_image = cv2.imread(str(image_path))
    #         # Get resized dimensions
    #         width = int(original_image.shape[1] * self.resize_factor)
    #         height = int(original_image.shape[0] * self.resize_factor)
    #         dim = (width, height)

    #         # Get resized image and save
    #         resized_image = cv2.resize(original_image, dim)
    #         resized_image_path = self.resize_dir_path / "rsz_{}".format(image_path.name)
    #         if resized_image_path.is_file():
    #             print("Resized image already exists:", resized_image_path.name)
    #         else:
    #             cv2.imwrite(str(resized_image_path), resized_image)
    #         break
    #     return 'temp'

    ### Private
