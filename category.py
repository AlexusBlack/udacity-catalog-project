from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from index import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    items = relationship('Item')

    def __init__(self, name):
        self.name = name
