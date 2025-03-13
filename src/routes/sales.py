from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.db.transaction import execute_transaction
from src.models.product import Product
from src.models.sale import Sale, SaleTransaction

router = APIRouter()


async def process_sale(db: AsyncSession, items: list[dict]):
    """
    Handles sale recording with multiple products.
    `items` should be a list of dicts like:
    [{"product_id": 1, "quantity": 3}, {"product_id": 2, "quantity": 2}]
    """

    if not items:
        raise HTTPException(status_code=400, detail="No products in sale")

    total_price = 0
    sale_items = []

    # Create transaction
    sale_transaction = SaleTransaction()
    db.add(sale_transaction)
    await db.flush()  # Get transaction ID

    for item in items:
        product_id, quantity = item["product_id"], item["quantity"]

        # Fetch product
        result = await db.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {product_id} not found")

        item_price = product.price * quantity
        total_price += item_price

        sale_items.append(
            Sale(transaction_id=sale_transaction.id, product_id=product_id, quantity=quantity, total_price=item_price)
        )

    # Add sale items and update total price
    sale_transaction.total_price = total_price
    db.add_all(sale_items)

    return {"message": "Sale recorded successfully", "total_price": total_price}


@router.post("/sales/")
async def create_sale(items: list[dict], db: AsyncSession = Depends(get_db)):
    """
    API endpoint to process a sale with multiple products.
    Expected JSON request:
    {
        "items": [
            {"product_id": 1, "quantity": 3},
            {"product_id": 2, "quantity": 2}
        ]
    }
    """
    return await execute_transaction(db, lambda session: process_sale(session, items))