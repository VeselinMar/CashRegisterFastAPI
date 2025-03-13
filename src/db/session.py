from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from src.database import DATABASE_URL

# Create an async database engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get an async DB session
@asynccontextmanager
async def get_db():
    """Dependency to provide an async session with transaction support."""
    async with AsyncSessionLocal() as session:
        try:
            yield session  # Provide session to the route
            await session.commit()  # Commit if successful
        except Exception as e:
            await session.rollback()  # Rollback if an error occurs
            raise e
        finally:
            await session.close()
