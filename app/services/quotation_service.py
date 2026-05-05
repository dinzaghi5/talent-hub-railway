from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, func
from typing import Optional, List
from datetime import date
from fastapi import HTTPException, status
from app.models.report import Report
from app.models.quotation import QuotationHeader
from app.models.brand import Brand
from app.models.quotation_detail import QuotationDetail
from app.models.sow import Sow
from app.models.social_media import SocialMedia
from app.schemas.quotation import QuotationCreate, QuotationUpdate, QuotationWithDetailCreate


class QuotationService:

    def _get_roman_month(self, month: int) -> str:
        roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
        return roman[month - 1]

    async def _generate_quotation_code(self, db: AsyncSession, brand_inisial: str = "DGM") -> str:
        """
        Generate quotation_code with format: QTN/BRAND/YEAR/MONTH/SEQ
        e.g. QTN/DGM/2026/V/001
        """
        today = date.today()
        year = today.year
        month_roman = self._get_roman_month(today.month)
        
        # Clean brand_inisial and use default if empty
        brand = (brand_inisial or "DGM").upper()
        
        prefix = f"QTN/{brand}/{year}/{month_roman}/"

        # Count existing codes with this prefix to get the next sequence
        result = await db.execute(
            select(func.count(QuotationHeader.id)).where(
                QuotationHeader.quotation_code.like(f"{prefix}%")
            )
        )
        count = result.scalar() or 0
        next_number = count + 1
        return f"{prefix}{next_number:03d}"

    async def get(self, db: AsyncSession, quotation_id: int) -> QuotationHeader | None:
        result = await db.execute(select(QuotationHeader).filter(QuotationHeader.id == quotation_id))
        return result.scalars().first()

    async def get_by_code(self, db: AsyncSession, quotation_code: str) -> QuotationHeader | None:
        result = await db.execute(select(QuotationHeader).filter(QuotationHeader.quotation_code == quotation_code))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, status_quotation: Optional[int] = None) -> list[QuotationHeader]:
        query = select(QuotationHeader)
        if status_quotation is not None:
            query = query.filter(QuotationHeader.status_quotation == status_quotation)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, obj_in: QuotationCreate) -> QuotationHeader:
        # Get brand initial from database
        brand_inisial = "DGM"
        if obj_in.brand_name:
            brand_result = await db.execute(select(Brand).filter(Brand.brand_nm == obj_in.brand_name))
            brand_obj = brand_result.scalars().first()
            if brand_obj and brand_obj.inisial:
                brand_inisial = brand_obj.inisial

        # Auto-generate quotation_code
        quotation_code = await self._generate_quotation_code(db, brand_inisial=brand_inisial)

        db_obj = QuotationHeader(
            quotation_code=quotation_code,
            invoice_code=obj_in.invoice_code,
            brand_name=obj_in.brand_name,
            status_quotation=obj_in.status_quotation,
            project=obj_in.project,
            quotation_date=obj_in.quotation_date,
            subtotal=obj_in.subtotal,
            dpp=obj_in.dpp,
            ppn=obj_in.ppn,
            grand_total=obj_in.grand_total,
            created_by="SYSTEM"
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_with_details(self, db: AsyncSession, obj_in: QuotationWithDetailCreate) -> QuotationHeader:
        # Validate Brand and get initial
        brand_result = await db.execute(select(Brand).filter(Brand.brand_nm == obj_in.brand_name))
        brand_obj = brand_result.scalars().first()
        if not brand_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Brand with name '{obj_in.brand_name}' not found in Master Brand database."
            )
        
        brand_inisial = brand_obj.inisial or "DGM"

        # Auto-generate quotation_code
        quotation_code = await self._generate_quotation_code(db, brand_inisial=brand_inisial)

        # Create Header
        db_header = QuotationHeader(
            quotation_code=quotation_code,
            invoice_code=obj_in.invoice_code,
            brand_name=obj_in.brand_name,
            status_quotation=obj_in.status_quotation,
            project=obj_in.project,
            quotation_date=obj_in.quotation_date,
            subtotal=obj_in.subtotal,
            dpp=obj_in.dpp,
            ppn=obj_in.ppn,
            grand_total=obj_in.grand_total,
            created_by="SYSTEM"
        )
        db.add(db_header)
        await db.flush()  # To get the header ID

        # Create Details
        for i, detail_in in enumerate(obj_in.details):
            # Validate SOW if provided
            if detail_in.sow_id is not None:
                sow_result = await db.execute(select(Sow).filter(Sow.sow_id == detail_in.sow_id))
                if not sow_result.scalars().first():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error at item {i+1}: SOW ID {detail_in.sow_id} not found in Master SOW."
                    )
            
            # Validate Social Media if provided
            if detail_in.id_medsos is not None:
                medsos_result = await db.execute(select(SocialMedia).filter(SocialMedia.social_media_id == detail_in.id_medsos))
                if not medsos_result.scalars().first():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error at item {i+1}: Social Media ID {detail_in.id_medsos} not found in Master Social Media."
                    )

            db_detail = QuotationDetail(
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
                total_cost=detail_in.total_cost,
                er=detail_in.er,
                avg_view=detail_in.avg_view,
                avg_brand_view=detail_in.avg_brand_view,
                created_by="SYSTEM"
            )
            db.add(db_detail)

        await db.commit()
        await db.refresh(db_header)
        return db_header

    async def update(self, db: AsyncSession, *, db_obj: QuotationHeader, obj_in: QuotationUpdate) -> QuotationHeader:
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Check if brand_name is being updated to trigger quotation_code update
        if "brand_name" in update_data and update_data["brand_name"] != db_obj.brand_name:
            new_brand_name = update_data["brand_name"]
            
            # Look up new brand's inisial
            brand_result = await db.execute(select(Brand).filter(Brand.brand_nm == new_brand_name))
            brand_obj = brand_result.scalars().first()
            
            if brand_obj and brand_obj.inisial:
                new_inisial = brand_obj.inisial.upper()
                
                # Parse current quotation_code: QTN/BRAND/YEAR/MONTH/SEQ
                old_code = db_obj.quotation_code
                parts = old_code.split("/")
                if len(parts) >= 5:
                    parts[1] = new_inisial # Update the brand part
                    new_code = "/".join(parts)
                    db_obj.quotation_code = new_code
                    
                    # Also update quotation_code in related reports
                    from sqlalchemy import update as sqlalchemy_update
                    await db.execute(
                        sqlalchemy_update(Report)
                        .where(Report.quotation_id == db_obj.id)
                        .values(quotation_code=new_code)
                    )

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_status(self, db: AsyncSession, *, db_obj: QuotationHeader, status: int) -> QuotationHeader:
        db_obj.status_quotation = status
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, quotation_id: int) -> QuotationHeader | None:
        obj = await self.get(db, quotation_id)
        if obj:
            # Delete related reports
            await db.execute(delete(Report).where(Report.quotation_id == quotation_id))

            await db.delete(obj)
            await db.commit()
        return obj


quotation_service = QuotationService()
