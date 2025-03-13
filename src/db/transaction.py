from sqlalchemy.ext.asyncio import AsyncSession

async def execute_transaction(db: AsyncSession, operations):
    """
    Executes a set of database operations as a transaction.
    Rolls back if any operation fails.

    """
    async with db.begin():  # Begin transaction
        try:
            result = await operations(db)  # Execute the provided operations
            await db.commit()  # Commit changes
            return result
        except Exception as e:
            await db.rollback()  # Rollback on error
            raise e  # Rethrow the exception
