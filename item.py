from sqlalchemy import Column, String, Integer, ForeignKey
from index import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, name, description):
        self.name = name
        self.description = description
