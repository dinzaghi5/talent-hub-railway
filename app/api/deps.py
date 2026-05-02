from typing import Generator
from app.db.session import AsyncSessionLocal

async def get_db() -> Generator:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
