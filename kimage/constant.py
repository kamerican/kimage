from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).parent
DATABASE_NAME = 'db.sqlite'
DATABASE_PATH = BASE_DIR / 'database' / DATABASE_NAME
DATABASE_URI = 'sqlite:///' + str(DATABASE_PATH)

# print(BASE_DIR, DATABASE_PATH, DATABASE_URI)
engine = create_engine(DATABASE_URI)
# print(engine)
session_factory = sessionmaker()
session_factory.configure(bind=engine)





