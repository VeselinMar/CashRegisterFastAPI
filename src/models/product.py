from sqlalchemy import Column, Integer, String, Float

from src.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, Unique=True, index=True)
    price = Column(Float)
    stock = Column(Integer)
