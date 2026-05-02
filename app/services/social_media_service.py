from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.social_media import SocialMedia
from app.schemas.social_media import SocialMediaCreate, SocialMediaUpdate

class SocialMediaService:
    async def get(self, db: AsyncSession, social_media_id: int) -> SocialMedia | None:
        result = await db.execute(select(SocialMedia).filter(SocialMedia.social_media_id == social_media_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[SocialMedia]:
        result = await db.execute(select(SocialMedia))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: SocialMediaCreate) -> SocialMedia:
        db_obj = SocialMedia(
            social_media_nm=obj_in.social_media_nm,
            base_url=obj_in.base_url,
            is_active=True,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: SocialMedia, obj_in: SocialMediaUpdate) -> SocialMedia:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, social_media_id: int) -> SocialMedia | None:
        obj = await self.get(db, social_media_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

social_media_service = SocialMediaService()
