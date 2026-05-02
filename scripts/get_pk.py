import asyncio
from sqlalchemy import text
from app.db.session import engine

async def get_pk():
    async with engine.connect() as conn:
        query = text("""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_name = 'tb_m_user';
        """)
        result = await conn.execute(query)
        pk = result.scalar()
        print(f"PRIMARY KEY: {pk}")

if __name__ == "__main__":
    asyncio.run(get_pk())
