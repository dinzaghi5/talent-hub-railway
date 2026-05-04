from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate

class BrandService:
    async def get(self, db: AsyncSession, brand_id: int) -> Brand | None:
        result = await db.execute(select(Brand).filter(Brand.brand_id == brand_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[Brand]:
        result = await db.execute(select(Brand))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: BrandCreate) -> Brand:
        db_obj = Brand(
            brand_nm=obj_in.brand_nm,
            brand_address=obj_in.brand_address,
            brand_company_name=obj_in.brand_company_name,
            brand_email=obj_in.brand_email,
            brand_pic_1=obj_in.brand_pic_1,
            brand_pic_2=obj_in.brand_pic_2,
            brand_pic_3=obj_in.brand_pic_3,
            inisial=obj_in.inisial,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Brand, obj_in: BrandUpdate) -> Brand:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, brand_id: int) -> Brand | None:
        obj = await self.get(db, brand_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

brand_service = BrandService()
