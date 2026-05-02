from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate

class CityService:
    async def get(self, db: AsyncSession, city_id: int) -> City | None:
        result = await db.execute(select(City).filter(City.city_id == city_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[City]:
        result = await db.execute(select(City))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CityCreate) -> City:
        db_obj = City(
            city_nm=obj_in.city_nm,
            country_id=obj_in.country_id,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: City, obj_in: CityUpdate) -> City:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, city_id: int) -> City | None:
        obj = await self.get(db, city_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

city_service = CityService()
