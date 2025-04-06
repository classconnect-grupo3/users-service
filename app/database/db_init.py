# db_init.py
from app.config.database.db import engine, Base


def initialize_database():
    Base.metadata.create_all(bind=engine)
