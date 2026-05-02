from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.list_creator_header import ListCreatorHeader
from app.schemas.list_creator_header import ListCreatorHeaderCreate, ListCreatorHeaderUpdate

class ListCreatorHeaderService:
    async def get(self, db: AsyncSession, id: int) -> ListCreatorHeader | None:
        result = await db.execute(select(ListCreatorHeader).filter(ListCreatorHeader.id == id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[ListCreatorHeader]:
        result = await db.execute(select(ListCreatorHeader))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: ListCreatorHeaderCreate) -> ListCreatorHeader:
        db_obj = ListCreatorHeader(
            name_list=obj_in.name_list,
            total_creator=obj_in.total_creator,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, objs_in: list[ListCreatorHeaderCreate]) -> list[ListCreatorHeader]:
        db_objs = [
            ListCreatorHeader(
                name_list=obj_in.name_list,
                total_creator=obj_in.total_creator,
                created_by="SYSTEM"
            )
            for obj_in in objs_in
        ]
        db.add_all(db_objs)
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        return db_objs

    async def update(self, db: AsyncSession, *, db_obj: ListCreatorHeader, obj_in: ListCreatorHeaderUpdate) -> ListCreatorHeader:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db_obj.changed_by = "SYSTEM"
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> ListCreatorHeader | None:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

list_creator_header_service = ListCreatorHeaderService()
