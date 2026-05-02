import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from app.db.session import AsyncSessionLocal
from sqlalchemy import text

async def check():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT * FROM tb_r_report LIMIT 0"))
            cols = result.keys()
            print("---START---")
            for col in cols:
                print(col)
            print("---END---")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check())
