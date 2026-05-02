import json
from unittest import result
from warnings import filters

import requests

from datetime import datetime, timedelta, timezone
from typing import Any, Counter, Dict
from sqlalchemy import delete, and_, false, update

# from fastapi import requests

from app.api import deps
from app.models.master_system import MasterSystem
Dict, 
from alembic.environment import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.kol import KOLDetailModel, KOLHeaderModel
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate
from app.schemas.kol import KOLBase, KOLCreate, KOLData, KOLHeader, KOLSearch, KOLUpdate, PostData
from app.models.report import Report

class MasterSystemService:

    async def update_system_value(self, db: AsyncSession, system_val: str, system_type: str, system_cd: str) -> MasterSystem | None:
        print(f"<==== service : {system_val} ====>")
        result =await db.execute(
            update(MasterSystem)
            .where(
                MasterSystem.system_type == system_type,
                MasterSystem.system_cd == system_cd
            )
            .values(system_val=system_val)
        )
        await db.commit()

        return result.rowcount
    
    async def get_system_value(self, db: AsyncSession, system_type: str, system_cd: str) -> MasterSystem | None:
        result = await db.execute(
            select(MasterSystem.system_val)
            .where(
                MasterSystem.system_type == system_type,
                MasterSystem.system_cd == system_cd
            )
        )
        system_val = result.scalar_one_or_none()
        print(f"<==== service get : {system_val} ====>")
        return system_val
master_system_service = MasterSystemService()
