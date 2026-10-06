from dotenv import load_dotenv # it import load_dotenv func from dotenv module
import os   # os is a python package that help us to interact with os level api  it import os module
from sqlalchemy import create_engine,MetaData # from sqlalchemy import create_engine,metadata function   create engine create a engine object that contain all the info that the sqlalchemy code need to communicate with the dataabse. it create a connection for the dataabse it allow sqlalchemy to communcicate with the database
from sqlalchemy.orm import sessionmaker
#ORM-> ORM allows you to work with database tables using Python classes and objects instead of writing SQL queries manually.
# SESSION MAKER-> Session is used to interact with the database through SQLAlchemy ORM
# You use a session to perform operations such as: INSERT,UPDATE,DELETE,SELECT
from sqlalchemy.ext.declarative import declarative_base

load_dotenv() # load environment variable form .env file
DATABASE_URL=os.getenv("DATABASE_URL")  #Get the database_url environment varibale

engine=create_engine(DATABASE_URL)  # create a sqlalchemy engine

metadata=MetaData()  # create a sqlalchemy metadata object  MetaData database ki tables ka structure/information store karta hai.

# Ye actual data store nahi karta. Ye database ke structure ka description rakhta hai.

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)  # creates a session factory that is used to create SQLAlchemy Session objects.

Base=declarative_base()  # create a sqlalchemy base object
