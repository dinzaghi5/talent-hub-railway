from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.list_creator_header import ListCreatorHeader
from app.models.list_creator_detail import ListCreatorDetail
from app.schemas.list_creator_header import ListCreatorHeaderCreate, ListCreatorHeaderUpdate, ListCreatorWithDetailCreate

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

    async def create_with_details(self, db: AsyncSession, obj_in: ListCreatorWithDetailCreate) -> ListCreatorHeader:
        # Create Header
        db_header = ListCreatorHeader(
            name_list=obj_in.name_list,
            total_creator=obj_in.total_creator,
            created_by="SYSTEM"
        )
        db.add(db_header)
        await db.flush()  # To get the header ID

        # Create Details
        for detail_in in obj_in.details:
            db_detail = ListCreatorDetail(
                header_id=db_header.id,
                link_foto=detail_in.link_foto,
                creator_name=detail_in.creator_name,
                creator_username=detail_in.creator_username,
                creator_post=detail_in.creator_post,
                followers=detail_in.followers,
                sow_id=detail_in.sow_id,
                quantity=detail_in.quantity,
                id_medsos=detail_in.id_medsos,
                rate=detail_in.rate,
                er=detail_in.er,
                avg_view=detail_in.avg_view,
                avg_brand_view=detail_in.avg_brand_view,
                created_by="SYSTEM"
            )
            db.add(db_detail)

        await db.commit()
        await db.refresh(db_header)
        return db_header

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
