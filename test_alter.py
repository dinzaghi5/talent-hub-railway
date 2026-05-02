import asyncio
from app.db.session import engine
from sqlalchemy import text

async def main():
    try:
        async with engine.begin() as conn:
            await conn.execute(text('ALTER TABLE tb_r_invoice_detail ADD COLUMN id SERIAL PRIMARY KEY;'))
        print("Success! Added id column.")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
