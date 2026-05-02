from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.quotation_detail import QuotationDetail
from app.schemas.quotation_detail import QuotationDetailCreate, QuotationDetailUpdate

class QuotationDetailService:
    async def get(self, db: AsyncSession, detail_id: int) -> QuotationDetail | None:
        result = await db.execute(select(QuotationDetail).filter(QuotationDetail.id == detail_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[QuotationDetail]:
        result = await db.execute(select(QuotationDetail))
        return list(result.scalars().all())

    async def get_by_header(self, db: AsyncSession, header_id: int) -> list[QuotationDetail]:
        result = await db.execute(select(QuotationDetail).filter(QuotationDetail.header_id == header_id))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: QuotationDetailCreate) -> QuotationDetail:
        db_obj = QuotationDetail(
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
            total_cost=obj_in.total_cost,
            er=obj_in.er,
            avg_view=obj_in.avg_view,
            avg_brand_view=obj_in.avg_brand_view,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_multi(self, db: AsyncSession, objs_in: list[QuotationDetailCreate]) -> list[QuotationDetail]:
        db_objs = [
            QuotationDetail(
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
                total_cost=obj_in.total_cost,
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

    async def update(self, db: AsyncSession, *, db_obj: QuotationDetail, obj_in: QuotationDetailUpdate) -> QuotationDetail:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, detail_id: int) -> QuotationDetail | None:
        obj = await self.get(db, detail_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

quotation_detail_service = QuotationDetailService()
