from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.list_creator_detail import ListCreatorDetail
from app.schemas.list_creator_detail import ListCreatorDetailCreate, ListCreatorDetailUpdate

class ListCreatorDetailService:
    async def get(self, db: AsyncSession, id: int) -> ListCreatorDetail | None:
        result = await db.execute(select(ListCreatorDetail).filter(ListCreatorDetail.id == id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[ListCreatorDetail]:
        result = await db.execute(select(ListCreatorDetail))
        return result.scalars().all()

    async def get_by_header(self, db: AsyncSession, header_id: int) -> list[ListCreatorDetail]:
        result = await db.execute(select(ListCreatorDetail).filter(ListCreatorDetail.header_id == header_id))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: ListCreatorDetailCreate) -> ListCreatorDetail:
        db_obj = ListCreatorDetail(
            header_id=obj_in.header_id,
            link_foto=obj_in.link_foto,
            creator_name=obj_in.creator_name,
            creator_username=obj_in.creator_username,
            creator_post=obj_in.creator_post,
            followers=obj_in.followers,
            sow_id=obj_in.sow_id,
            quantity=obj_in.quantity,
            id_medsos=obj_in.id_medsos,
            rate=obj_in.rate,
            er=obj_in.er,
            avg_view=obj_in.avg_view,
            avg_brand_view=obj_in.avg_brand_view,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, objs_in: list[ListCreatorDetailCreate]) -> list[ListCreatorDetail]:
        db_objs = [
            ListCreatorDetail(
                header_id=obj_in.header_id,
                link_foto=obj_in.link_foto,
                creator_name=obj_in.creator_name,
                creator_username=obj_in.creator_username,
                creator_post=obj_in.creator_post,
                followers=obj_in.followers,
                sow_id=obj_in.sow_id,
                quantity=obj_in.quantity,
                id_medsos=obj_in.id_medsos,
                rate=obj_in.rate,
                er=obj_in.er,
                avg_view=obj_in.avg_view,
                avg_brand_view=obj_in.avg_brand_view,
                created_by="SYSTEM"
            )
            for obj_in in objs_in
        ]
        db.add_all(db_objs)
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        return db_objs

    async def update(self, db: AsyncSession, *, db_obj: ListCreatorDetail, obj_in: ListCreatorDetailUpdate) -> ListCreatorDetail:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db_obj.changed_by = "SYSTEM"
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> ListCreatorDetail | None:
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

list_creator_detail_service = ListCreatorDetailService()
