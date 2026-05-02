from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.services.user_service import user_service
from app.services.pdf_service import pdf_service
from app.services.excel_service import excel_service
from app.api.v1.endpoints.export import ReportRequest, SAMPLE_DATA
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union, List

router = APIRouter()

# ── Schema for Report Detail ──────────────────────────────────────────────────
class ReportDetailItem(BaseModel):
    image_url: Optional[str] = None
    caption: Optional[str] = "No caption provided."
    likes: Union[int, str] = "-"
    comments: Union[int, str] = "-"
    saves: Union[int, str] = "-"
    reposts: Union[int, str] = "-"
    views: Union[int, str] = "-"
    plays: Union[int, str] = "-"
    duration: Union[int, str] = "-"
    avg_watch_time: Union[int, str] = "-"
    shares: Union[int, str] = "-"

class MultiReportDetailRequest(BaseModel):
    items: List[ReportDetailItem]
    username: Optional[str] = None
    project: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "image_url": "https://example.com/thumbnail.jpg",
                        "caption": "How does someone go from being everything to nothing... #emotionaltruth #blender",
                        "likes": 42729,
                        "comments": 59,
                        "saves": "-",
                        "reposts": "-",
                        "views": 165678,
                        "plays": 389517,
                        "duration": 10,
                        "avg_watch_time": 8,
                        "shares": 10
                    }
                ],
                "username": "Donna Bella",
                "project": "Project A"
            }
        }

@router.get("/kol/{user_id}")
async def generate_kol_pdf(
    user_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Generate PDF for a KOL user.
    """
    user = await user_service.get(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    pdf_buffer = pdf_service.create_kol_pdf(user)
    
    # Construct filename: KOL_FULLNAME_YEAR_ID.pdf
    # Handle None values appropriately
    fullname = user.fullname.replace(" ", "_").upper() if user.fullname else "UNKNOWN"
    year = user.created_dt.year if user.created_dt else "0000"
    filename = f"KOL_{fullname}_{year}_{user.user_id}.pdf"
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers=headers
    )

from app.schemas.pdf import QuotationCreate, QuotationCreateNoPic

@router.post("/quotation")
async def generate_quotation_pdf(
    data: QuotationCreate
):
    """
    Generate Quotation PDF based on input data.
    """
    pdf_buffer = pdf_service.create_quotation_pdf(data)
    
    # Construct filename: QUOTATION - Quotation No (or just QUOTATION if empty)
    if data.quotation_no:
        filename = f"QUOTATION - {data.quotation_no}.pdf"
    else:
        filename = "QUOTATION.pdf"
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers=headers
    )

@router.post("/quotation/pic1", tags=["quotation"])
async def generate_quotation_pic1(data: QuotationCreateNoPic):
    """Generate Quotation PDF with 1 Signature Column (PIC 1) — pic_count otomatis = 1"""
    return await generate_quotation_pdf(data.to_quotation_create(pic_count=1))

@router.post("/quotation/pic2", tags=["quotation"])
async def generate_quotation_pic2(data: QuotationCreateNoPic):
    """Generate Quotation PDF with 2 Signature Columns (PIC 2) — pic_count otomatis = 2"""
    return await generate_quotation_pdf(data.to_quotation_create(pic_count=2))

@router.post("/quotation/pic3", tags=["quotation"])
async def generate_quotation_pic3(data: QuotationCreateNoPic):
    """Generate Quotation PDF with 3 Signature Columns (PIC 3) — pic_count otomatis = 3"""
    return await generate_quotation_pdf(data.to_quotation_create(pic_count=3))

@router.post("/spreadsheet/report", tags=["report"])
async def generate_report_spreadsheet(request: ReportRequest):
    """
    Generate Spreadsheet Report (CSV) from a list of items in the request body.
    """
    if request.items:
        data = [item.to_formatted_dict() for item in request.items]
    else:
        data = SAMPLE_DATA

    csv_buffer = excel_service.create_tabel_csv(data)
    if request.list_name:
        filename = f"LIST CREATOR - {request.list_name}.csv"
    else:
        names_str = " - ".join([item.nama for item in request.items]) if request.items else "SAMPLE"
        filename = f"LIST CREATOR - {names_str}.csv"
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(
        csv_buffer, 
        media_type="text/csv", 
        headers=headers
    )

@router.post("/report-detail", tags=["report"])
async def generate_report_detail(data: MultiReportDetailRequest):
    """
    Generate PDF Report Detail with content image, caption, and performance metrics.

    - **image_url**: URL gambar konten (optional, akan muncul placeholder jika kosong)
    - **caption**: Teks caption konten
    - **likes / comments / saves / reposts**: Engagement metrics
    - **views / plays / duration / shares**: View metrics
    """
    pdf_buffer = pdf_service.create_detail_pdf(data)
    
    if len(data.items) == 1:
        filename = f"INSIGHT - {data.username}.pdf" if data.username else "INSIGHT.pdf"
    else:
        filename = f"INSIGHT - {data.project}.pdf" if data.project else "INSIGHT.pdf"

    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers=headers
    )
