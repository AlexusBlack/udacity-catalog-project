"""
ORM mapping to categories table in DB
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from base import Base

class Category(Base):
    """
    Category contains items,
    also it has name to be nicely called
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    items = relationship('Item', cascade="all, delete")

    def __init__(self, name):
        self.name = name

    # We need able convert this object to JSON for our API
    def serialize(self):
        """
        Convert the category into JSON serializable object
        """
        return {
            'id': self.id,
            'name': self.name
        }
