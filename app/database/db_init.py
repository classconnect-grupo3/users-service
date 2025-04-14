# db_init.py
from app.database.db import Base, engine


def initialize_database():
    Base.metadata.create_all(bind=engine)
