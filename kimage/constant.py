from pathlib import Path

BASE_DIR = Path(__file__).parent
DATABASE_NAME = 'shelve'
DATABASE_PATH = BASE_DIR / 'database' / DATABASE_NAME
DATABASE = str(DATABASE_PATH)
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
