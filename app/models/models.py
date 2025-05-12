from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    sales = relationship("Sale", back_populates="product")

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True)
    stock = Column(Integer, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    product = relationship("Product", back_populates="inventory")

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    sold_at = Column(DateTime, server_default=func.now())
    product = relationship("Product", back_populates="sales")
