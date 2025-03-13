from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.database import Base


class SaleTransaction(Base):
    """Represents a single sale event that can include multiple products."""
    __tablename__ = "sale_transactions"

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float, nullable=False, default=0.0)

    # Relationship to link individual sale items
    sale_items = relationship("Sale", back_populates="transaction")


class Sale(Base):
    """Represents a single product sold in a sale transaction."""
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("sale_transactions.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)

    # Relationship
    transaction = relationship("SaleTransaction", back_populates="sale_items")
