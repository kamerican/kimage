from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# 'sqlite:///:memory:'

BASE_DIR = Path(__file__).parent
DATABASE_NAME = 'db.sqlite'
DATABASE_PATH = BASE_DIR / 'database' / DATABASE_NAME
DATABASE_URI = 'sqlite:///' + str(DATABASE_PATH)

PICTURE_FILE_STRING_LENGTH = 19
PICTURE_NAME_STRING_LENGTH = 15

# print(BASE_DIR, DATABASE_PATH, DATABASE_URI)
engine = create_engine(DATABASE_URI, echo=False)
# print(engine)
session_factory = sessionmaker()
session_factory.configure(bind=engine)

# session = session_factory()
# print(type(session))

IDOL_DICT = {
    'WJSN': [
        'Seola',
        'Xuanyi',
        'Bona',
        'Exy',
        'Soobin',
        'Luda',
        'Dawon',
        'Eunseo',
        'Chengxiao',
        'Meiqi',
        'Yeoreum',
        'Dayoung',
        'Yeonjung',
    ],
    'fromis_9': [
        'Saerom',
    ],
    'Red Velvet': [
        'Irene',
        'Wendy',
        'Seulgi',
    ],
    'Rocket Girls': [
        'Zining',
    ],
    'IZONE': [
        'Yujin',
        'Yena',
    ],
}
