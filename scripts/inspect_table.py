import asyncio
from sqlalchemy import text
from app.db.session import engine

async def inspect_user_table():
    async with engine.connect() as conn:
        # Get columns for tb_m_user
        query = text("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'tb_m_user'
        """)
        result = await conn.execute(query)
        columns = result.fetchall()
        
        print("\n=== STRUKTUR TABEL tb_m_user ===")
        for col in columns:
            print(f"Column: {col[0]} | Type: {col[1]} | Nullable: {col[2]}")
        print("================================\n")

if __name__ == "__main__":
    asyncio.run(inspect_user_table())
