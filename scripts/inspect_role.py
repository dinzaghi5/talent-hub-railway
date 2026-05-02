import asyncio
from sqlalchemy import text
from app.db.session import engine

async def inspect_role_table():
    async with engine.connect() as conn:
        query = text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'tb_m_role'
        """)
        result = await conn.execute(query)
        columns = result.fetchall()
        
        print("\n=== STRUKTUR TABEL tb_m_role ===")
        for col in columns:
            print(f"Column: {col[0]} | Type: {col[1]} | Nullable: {col[2]}")
        print("================================\n")

if __name__ == "__main__":
    asyncio.run(inspect_role_table())
