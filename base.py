"""
Basic database configiration,
every file using database will import this file
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# just connecting to local database `catalog`
engine = create_engine('postgresql:///catalog')
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()
