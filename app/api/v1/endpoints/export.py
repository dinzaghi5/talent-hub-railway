from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from app.services.pdf_service import pdf_service
from app.services.excel_service import excel_service
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ReportItemModel(BaseModel):
    nama: str = "Gansa"
    username: str = "Gansa.jkt"
    post: int = 9
    follower: int = 83000
    er: str = "1.69%"
    avg_view_all_content: str = "22,340"
    avg_view_branded_content: str = "18,200"
    rate: str = "8,500,000"
    cpv_all_content: str = "-"
    cpv_branded_content: str = "-"

    def to_formatted_dict(self):
        return {
            "NAMA": self.nama,
            "Username": self.username,
            "Post": self.post,
            "Followers": f"{self.follower:,}",
            "ER": self.er,
            "Avg view all content": self.avg_view_all_content,
            "Avg view branded content": self.avg_view_branded_content,
            "Rate": self.rate,
            "Cost per view all content": self.cpv_all_content,
            "Cost per view branded content": self.cpv_branded_content
        }

class ReportRequest(BaseModel):
    list_name: Optional[str] = None
    items: List[ReportItemModel]

class ReportItemModelNewDiscovery(BaseModel):
    nama: str = "Gansa"
    username: str = "Gansa.jkt"
    post: int = 9
    follower: int = 83000
    avg_view_all_content: str = "22,340"
    avg_view_branded_content: str = "18,200"
    rate: str = "8,500,000"
    cpv_all_content: str = "-"
    cpv_branded_content: str = "-"

    def to_formatted_dict(self):
        return {
            "NAMA": self.nama,
            "Username": self.username,
            "Post": self.post,
            "Followers": f"{self.follower:,}",
            "Avg view all content": self.avg_view_all_content,
            "Avg view branded content": self.avg_view_branded_content,
            "Rate": self.rate,
            "Cost per view all content": self.cpv_all_content,
            "Cost per view branded content": self.cpv_branded_content
        }

class ReportRequestNewDiscovery(BaseModel):
    list_name: Optional[str] = None
    items: List[ReportItemModelNewDiscovery]

# Sample data based on the provided format
SAMPLE_DATA = [
    {
        "NAMA": "Gansa",
        "Username": "Gansa.jkt",
        "Post": 9,
        "Followers": "83,000",
        "ER": "1.69%",
        "Avg view all content": "22,340",
        "Avg view branded content": "18,200",
        "Rate": "8,500,000",
        "Cost per view all content": "380",
        "Cost per view branded content": "467"
    },
    {
        "NAMA": "Lutfi Afansyah",
        "Username": "lutfiafansyahh",
        "Post": 15,
        "Followers": "268,000",
        "ER": "4.18%",
        "Avg view all content": "254,920",
        "Avg view branded content": "224,200",
        "Rate": "30,000,000",
        "Cost per view all content": "118",
        "Cost per view branded content": "134"
    },
    {
        "NAMA": "Tissa Biani",
        "Username": "tissabiani",
        "Post": 22,
        "Followers": "5,400,000",
        "ER": "0.66%",
        "Avg view all content": "443,540",
        "Avg view branded content": "202,860",
        "Rate": "65,000,000",
        "Cost per view all content": "147",
        "Cost per view branded content": "320"
    }
]

SAMPLE_DATA_NO_ER = [
    {k: v for k, v in item.items() if k != "ER"} for item in SAMPLE_DATA
]


@router.post("/pdf/report")
async def generate_report_pdf(request: ReportRequest):
    """
    Generate PDF Report from a list of items in the request body.
    """
    if request.items:
        data = [item.to_formatted_dict() for item in request.items]
    else:
        data = SAMPLE_DATA

    if request.list_name:
        base_name = f"LIST CREATOR - {request.list_name}"
    else:
        names_str = " - ".join([item.nama for item in request.items]) if request.items else "SAMPLE"
        base_name = f"LIST CREATOR - {names_str}"
        
    filename = f"{base_name}.pdf"
    pdf_buffer = pdf_service.create_tabel_pdf(data, report_title=base_name)

    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers=headers
    )

@router.post("/excel/report")
async def generate_report_excel(request: ReportRequest):
    """
    Generate Excel Report from a list of items in the request body.
    """
    if request.items:
        data = [item.to_formatted_dict() for item in request.items]
    else:
        data = SAMPLE_DATA

    excel_buffer = excel_service.create_tabel_excel(data)
    if request.list_name:
        filename = f"LIST CREATOR - {request.list_name}.xlsx"
    else:
        names_str = " - ".join([item.nama for item in request.items]) if request.items else "SAMPLE"
        filename = f"LIST CREATOR - {names_str}.xlsx"
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(
        excel_buffer, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers=headers
    )

@router.post("/pdf/reportNewDiscovery")
async def generate_report_pdf_new_discovery(request: ReportRequestNewDiscovery):
    """
    Generate PDF Report without ER column (New Discovery format).
    """
    if request.items:
        data = [item.to_formatted_dict() for item in request.items]
    else:
        data = SAMPLE_DATA_NO_ER

    if request.list_name:
        base_name = f"LIST CREATOR - {request.list_name} (NEW DISCOVERY)"
    else:
        names_str = " - ".join([item.nama for item in request.items]) if request.items else "SAMPLE"
        base_name = f"LIST CREATOR - {names_str} (NEW DISCOVERY)"
        
    filename = f"{base_name}.pdf"
    pdf_buffer = pdf_service.create_tabel_pdf(data, report_title=base_name)

    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers=headers
    )

@router.post("/excel/reportNewDiscovery")
async def generate_report_excel_new_discovery(request: ReportRequestNewDiscovery):
    """
    Generate Excel Report without ER column (New Discovery format).
    """
    if request.items:
        data = [item.to_formatted_dict() for item in request.items]
    else:
        data = SAMPLE_DATA_NO_ER

    excel_buffer = excel_service.create_tabel_excel(data)
    if request.list_name:
        filename = f"LIST CREATOR - {request.list_name} (NEW DISCOVERY).xlsx"
    else:
        names_str = " - ".join([item.nama for item in request.items]) if request.items else "SAMPLE"
        filename = f"LIST CREATOR - {names_str} (NEW DISCOVERY).xlsx"
    
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(
        excel_buffer, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers=headers
    )
