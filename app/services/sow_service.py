from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.sow import Sow
from app.schemas.sow import SowCreate, SowUpdate

class SowService:
    async def get(self, db: AsyncSession, sow_id: int) -> Sow | None:
        result = await db.execute(select(Sow).filter(Sow.sow_id == sow_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[Sow]:
        result = await db.execute(select(Sow))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: SowCreate) -> Sow:
        db_obj = Sow(
            sow_nm=obj_in.sow_nm,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Sow, obj_in: SowUpdate) -> Sow:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, sow_id: int) -> Sow | None:
        obj = await self.get(db, sow_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

sow_service = SowService()
