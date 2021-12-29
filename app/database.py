from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# import psycopg2
# import psycopg2.extras
# import time

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         # Connect to your postgres DB
#         conn = psycopg2.connect(
#             host="localhost",
#             database="",
#             user="",
#             password="",
#         )
#         # Open a cursor to perform database operations
#         cur = conn.cursor()
#         print("Connected to a database!")
#         break

#     except Exception as error:
#         print("Error connecting to the database")
#         print("Error ", error)
#         time.sleep(2)
