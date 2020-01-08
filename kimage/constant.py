from pathlib import Path


BASE_DIR = Path(__file__).parent
DRIVE_NAME = "F:"
DATA_DIR = Path(DRIVE_NAME).joinpath('data')
IMAGE_DIR = DATA_DIR.joinpath('images')
DUMP_DIR = DATA_DIR.joinpath('dump')
# for c in DATA_DIR.iterdir(): print(c)
