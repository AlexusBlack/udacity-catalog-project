from sqlalchemy import Column, String, Integer, ForeignKey
from base import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id
        }