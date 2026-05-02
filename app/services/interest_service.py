from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.interest import Interest
from app.schemas.interest import InterestCreate, InterestUpdate

class InterestService:
    async def get(self, db: AsyncSession, interest_id: int) -> Interest | None:
        result = await db.execute(select(Interest).filter(Interest.interest_id == interest_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[Interest]:
        result = await db.execute(select(Interest))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: InterestCreate) -> Interest:
        db_obj = Interest(
            interest_nm=obj_in.interest_nm,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Interest, obj_in: InterestUpdate) -> Interest:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, interest_id: int) -> Interest | None:
        obj = await self.get(db, interest_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

interest_service = InterestService()
