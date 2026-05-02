import asyncio
from sqlalchemy import text
from app.db.session import engine

async def seed_roles():
    async with engine.begin() as conn:
        # Check if role exists
        result = await conn.execute(text("SELECT role_id FROM tb_m_role WHERE role_nm = 'Admin'"))
        if result.scalar():
            print("Role 'Admin' sudah ada.")
            return

        # Insert Role
        await conn.execute(text("INSERT INTO tb_m_role (role_id, role_nm) VALUES (1, 'Admin')"))
        print("Berhasil membuat Role: Admin (ID: 1)")

if __name__ == "__main__":
    asyncio.run(seed_roles())
