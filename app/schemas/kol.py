from pydantic import BaseModel  
from typing import Any, List, Optional
from datetime import datetime

class KOLBase(BaseModel):
    # kol_id: Optional[int] = None
    kol_account: Optional[str] = None
    total_post: Optional[float] = 0
    avg_like: Optional[float] = 0
    avg_comment: Optional[float] = 0
    avg_reach: Optional[float] = 0
    avg_view: Optional[float] = 0
    avg_brand_view: Optional[float] = 0
    er: Optional[float] = 0
    avg_watch_time: Optional[float] = 0
    last_update: Optional[datetime] = None
    days: Optional[str] = None
    top_hashtags: Optional[str] = None
    top_mentions: Optional[str] = None
    socmed_type: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class KOLCreate(KOLBase):
    kol_account: str

class KOLUpdate(KOLBase):
    pass

class KOLHeader(BaseModel):
    kol_account: str = None
    kol_name: Optional[str] = None
    bio: Optional[str] = None
    bussiness_category: Optional[str] = None
    followers: Optional[int] = 0
    following: Optional[int] = 0
    profile_picture: Optional[str] = None
    last_update: Optional[datetime] = datetime.now()
    last_post: Optional[str] = None,
    socmed_type: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class KOLPost(BaseModel):
    kol_account: str
    post_url: Optional[str] = None
    caption: Optional[str] = None
    hashtags: Optional[list] = None
    taggedUsers: Optional[list] = None
    likeCount: Optional[int] = None
    commentCount: Optional[int] = None
    viewCount: Optional[int] = None
    playCount: Optional[int] = None
    duration: Optional[float] = 0


class KOLData(BaseModel):
    header: Optional[KOLHeader] = None
    detail: Optional[KOLBase] = None
    error_message: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
    
class BaseResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
class KOLResponse(BaseResponse):
    data: Optional[KOLData] = None

class KOLSearch(BaseModel):
    no: Optional[int] = None
    profile_picture: Optional[str] = None
    kol_name : Optional[str] = None
    kol_account: Optional[str] = None
    total_post: Optional[float] = 0
    total_follower: Optional[int] = 0
    er: Optional[float] = 0
    avg_view: Optional[float] = 0
    avg_brand_view: Optional[float] = 0

class KOLResponseList(BaseResponse):
    data: Optional[List[KOLSearch]] = None

class PostData(BaseModel):
    post_url: Optional[str] = None
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None
    taggedUsers: Optional[List[str]] = None
    likeCount: Optional[int] = None
    commentCount: Optional[int] = None
    viewCount: Optional[int] = None
    playCount: Optional[int] = None
    duration: Optional[float] = 0
    displayUrl: Optional[str] = None
    shareCount: Optional[int] = None
    repostCount: Optional[int] = None
    saveCount: Optional[int] = None
    avg_watch_time: Optional[str] = None