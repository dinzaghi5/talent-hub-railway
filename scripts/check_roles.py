import asyncio
from sqlalchemy import text
from app.db.session import engine

async def check_roles():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT role_id, role_nm FROM tb_m_role"))
        roles = result.fetchall()
        print("\n=== DAFTAR ROLE ===")
        if not roles:
            print("TIDAK ADA DATA ROLE. Harap buat role terlebih dahulu.")
        for role in roles:
            print(f"ID: {role[0]} | Name: {role[1]}")
        print("===================\n")

if __name__ == "__main__":
    asyncio.run(check_roles())
