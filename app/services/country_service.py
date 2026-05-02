from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.country import Country
from app.schemas.country import CountryCreate, CountryUpdate

class CountryService:
    async def get(self, db: AsyncSession, country_id: int) -> Country | None:
        result = await db.execute(select(Country).filter(Country.country_id == country_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[Country]:
        result = await db.execute(select(Country))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CountryCreate) -> Country:
        db_obj = Country(
            country_nm=obj_in.country_nm,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Country, obj_in: CountryUpdate) -> Country:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, country_id: int) -> Country | None:
        obj = await self.get(db, country_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

country_service = CountryService()
