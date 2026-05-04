import datetime
import requests
from datetime import timezone, timedelta
from collections import Counter

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import false
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.api.v1.endpoints import brand
from app.schemas.brand import BrandCreate, BrandResponse, BrandUpdate
from app.schemas.kol import KOLBase, KOLData, KOLHeader, KOLResponse, KOLResponseList, PostData
from app.services.master_system_service import master_system_service
from app.services.brand_service import brand_service
from app.services.kol_service import kol_service
from datetime import datetime
from typing import Any, Dict, List

router = APIRouter()


@router.get("/apify/{kol_account}", response_model=KOLResponse)
async def fetch_kol_from_external_api(
    kol_account: str,
    socmed_type: str,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get KOL Data from Apify
    """
    result = await kol_service.get_kol_data(db, kol_account=kol_account, socmed_type=socmed_type)

    #get data detail
    return result

@router.get("/db/", response_model=KOLResponse)
async def fetch_kol_from_external_api(
    kol_account: str,
    socmed_type: str,
    days: str = "90",
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get KOL Data from DB
    """

    print(f"<==== Fetching KOL data from DB for account: {kol_account} with days: {days}")
    detail = await kol_service.get_detail_by_account(db, kol_account=kol_account, days=days, socmed_type=socmed_type)
    header = await kol_service.get_header_by_account(db, kol_account=kol_account, socmed_type=socmed_type)
    #get data detail
    return KOLResponse(
        code=200,
        message="Success",
        data=(KOLData(
            header=header if header else KOLHeader(),
            detail=detail if detail else KOLBase())
        )
    )

@router.get("/GetList/", response_model=KOLResponseList)
async def get_kol_list(
    kol_account: str = "",
    min_avg_like: float = 0,
    max_avg_like: float = 0,
    min_followers: int = 0,
    max_followers: int = 0,
    hashtag: str = "",
    socmed_type: str = "",
    short_by: str = "ER",
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get KOL List from DB
    """

    print(f"<==== Fetching KOL list from DB")
    result = await kol_service.get_kol_list(
        db,
        kol_account=kol_account,
        min_avg_like=min_avg_like,
        max_avg_like=max_avg_like,
        min_followers=min_followers,
        max_followers=max_followers,
        hashtag=hashtag,
        socmed_type=socmed_type
        # ,
        # short_by=short_by
    )
    #get data detail
    return KOLResponseList(
        code=200,
        message="Success",
        data=result
    )

@router.get("/GetPostData", response_model=PostData)
async def get_kol_post_data(
    id: str,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get KOL Post Data from Apify
    """

    print(f"<==== Fetching KOL post data from Apify for post ID: {id}")
    result = await kol_service.get_data_post(db=db, id=id)
    #get data detail
    return result

@router.put("/UpdateSetting/")
async def update_kol_setting(
    system_val: str,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Update KOL Setting in DB
    """
    system_type = "KOL_SETTINGS"
    system_cd = "REFRESH_PERIOD"
    print(f"<==== Updating KOL setting in DB with value: {system_val}, type: {system_type}, code: {system_cd} ====>")
    result = await master_system_service.update_system_value(db=db, system_val=system_val, system_type=system_type, system_cd=system_cd)
    
    if result == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found or no changes made")
    
    return {
        "code": 200,
        "message": "Setting updated successfully",
        "data": {"updated_rows": result}
    }

@router.get("/GetSetting/")
async def get_kol_setting(
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Get KOL Setting from DB
    """
    system_type = "KOL_SETTINGS"
    system_cd = "REFRESH_PERIOD"
    print(f"<==== Fetching KOL setting from DB with type: {system_type}, code: {system_cd} ====>")
    result = await master_system_service.get_system_value(db=db, system_type=system_type, system_cd=system_cd)

    if result == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found or no changes made")
    
    return {
        "code": 200,
        "message": "Setting fetched successfully",
        "data": {"system_val": result}
    }