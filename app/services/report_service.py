from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate

class ReportService:
    async def get(self, db: AsyncSession, report_id: int) -> Report | None:
        result = await db.execute(select(Report).filter(Report.id == report_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[Report]:
        result = await db.execute(select(Report))
        return list(result.scalars().all())

    async def get_multi_by_quotation_code(self, db: AsyncSession, quotation_code: str) -> list[Report]:
        result = await db.execute(select(Report).filter(Report.quotation_code == quotation_code))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: ReportCreate) -> Report:
        db_obj = Report(
            name=obj_in.name,
            link=obj_in.link,
            followers=obj_in.followers,
            er=obj_in.er,
            avg_view_all_content=obj_in.avg_view_all_content,
            avg_view_branded_content=obj_in.avg_view_branded_content,
            rate_reels=obj_in.rate_reels,
            rate=obj_in.rate,
            creator_username=obj_in.creator_username,
            quotation_id=obj_in.quotation_id,
            quotation_code=obj_in.quotation_code,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: Report, obj_in: ReportUpdate) -> Report:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, report_id: int) -> Report | None:
        obj = await self.get(db, report_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

report_service = ReportService()
