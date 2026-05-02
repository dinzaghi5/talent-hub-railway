from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.schemas.report import ReportCreate, ReportResponse, ReportUpdate
from app.services.report_service import report_service

router = APIRouter()

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_in: ReportCreate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Create a new report.
    """
    return await report_service.create(db, obj_in=report_in)

@router.get("/", response_model=List[ReportResponse])
async def read_reports(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve reports.
    """
    return await report_service.get_multi(db)

@router.get("/by-quotation/{quotation_code}", response_model=List[ReportResponse])
async def read_reports_by_quotation(
    quotation_code: str,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve reports by quotation code.
    """
    return await report_service.get_multi_by_quotation_code(db, quotation_code=quotation_code)

@router.get("/{report_id}", response_model=ReportResponse)
async def read_report(
    report_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get report by ID.
    """
    report = await report_service.get(db, report_id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    return report

@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: int,
    report_in: ReportUpdate,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update a report.
    """
    report = await report_service.get(db, report_id=report_id)
    if not report:   
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    report = await report_service.update(db, db_obj=report, obj_in=report_in)
    return report

@router.delete("/{report_id}", response_model=ReportResponse)
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Delete a report.
    """
    report = await report_service.get(db, report_id=report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    await report_service.delete(db, report_id=report_id)
    return report
