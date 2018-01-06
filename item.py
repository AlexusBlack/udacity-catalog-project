"""
ORM mapping to items table
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from base import Base


class Item(Base):
    """
    Represents single row in items table
    """
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    owner = Column(String)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, name, description, owner='Admin'):
        self.name = name
        self.description = description
        self.owner = owner

    def serialize(self):
        """
        We need to serialize the object for our API endpoints
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id
        }
