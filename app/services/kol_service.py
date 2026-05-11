import json
from unittest import result
from warnings import filters

import cloudinary
from app.core.config import settings

import requests

from datetime import datetime, timedelta, timezone
from typing import Any, Counter, Dict
from sqlalchemy import delete, and_, false

# from fastapi import requests

from app.api import deps
from app.services.master_system_service import master_system_service
Dict, 
from alembic.environment import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.kol import KOLDetailModel, KOLHeaderModel
from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate
from app.schemas.kol import KOLBase, KOLCreate, KOLData, KOLHeader, KOLSearch, KOLUpdate, PostData
from app.models.report import Report

class KOLService:

    async def get_detail_by_account(self, db: AsyncSession, kol_account: str, days: str = "90", socmed_type: str = "") -> KOLBase | None:
        print(f"<==== service : {kol_account} | Days: {days} | Socmed Type: {socmed_type}")
        result = await db.execute(
                select(KOLDetailModel).where(
                    KOLDetailModel.kol_account == kol_account,
                    KOLDetailModel.days == days,
                    KOLDetailModel.socmed_type == socmed_type
                )
            )
        return result.scalars().first()
    
    async def delete_by_account(self, db: AsyncSession, kol_account: str, socmed_type: str = "") -> KOLDetailModel | None:
        await db.execute(
            delete(KOLDetailModel).where(
                KOLDetailModel.kol_account == kol_account,
                KOLDetailModel.socmed_type == socmed_type
            )
        )
        await db.commit()

        return True
    
    async def get_header_by_account(self, db: AsyncSession, kol_account: str, socmed_type: str = "") -> KOLHeader | None:
        header = (
                    await db.execute(
                        select(KOLHeaderModel)
                        .where(
                            KOLHeaderModel.kol_account == kol_account,
                            KOLHeaderModel.socmed_type == socmed_type
                        )
                        .order_by(KOLHeaderModel.last_update.desc())
                        .limit(1)
                    )
                ).scalars().first()
        return header

    async def create(self, db: AsyncSession, obj_in: KOLCreate) -> KOLBase:
        db_obj = KOLDetailModel(
            kol_account=obj_in["kol_account"],
            total_post=obj_in["total_post"],
            avg_like=obj_in["avg_like"],
            avg_comment=obj_in["avg_comment"],
            avg_reach=obj_in["avg_reach"],
            avg_view=obj_in["avg_view"],
            avg_brand_view=obj_in["avg_brand_view"],
            er=obj_in["er"],
            avg_watch_time=obj_in["avg_watch_time"],
            last_update=obj_in["last_update"],
            days=obj_in["days"],
            top_hashtags=obj_in["top_hashtags"],
            top_mentions=obj_in["top_mentions"],
            socmed_type=obj_in["socmed_type"],

            created_by="system",  # contoh, bisa diganti dengan user yang sebenarnya
            created_dt=datetime.utcnow()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def insertHeader(self, db: AsyncSession, obj_in: KOLHeader) -> KOLHeaderModel:
        db_obj = KOLHeaderModel(
            kol_account=obj_in.kol_account,
            kol_name=obj_in.kol_name,
            bio=obj_in.bio,
            bussiness_category=obj_in.bussiness_category,
            followers=obj_in.followers,
            following=obj_in.following,
            profile_picture=obj_in.profile_picture,
            last_update=obj_in.last_update,
            last_post=obj_in.last_post,
            socmed_type=obj_in.socmed_type,

            created_by="system",  # contoh, bisa diganti dengan user yang sebenarnya
            created_dt=datetime.utcnow()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def call_apify(self, payload: Dict[str, Any], actor_id: str) -> List[Dict[str, Any]]:
        print(f"<==== Calling Apify Actor: {actor_id} with payload: {payload}")
        APIFY_TOKEN = settings.APIFY_TOKEN

        ACTOR_ID = actor_id  # contoh: username~actor-name

        BASE_URL = "https://api.apify.com/v2"
        now = datetime.now(timezone.utc)
        
        run_url = f"{BASE_URL}/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}&waitForFinish=120"
        input_payload = payload

        response = requests.post(run_url, json=input_payload)
        response.raise_for_status()

        run_data = response.json()["data"]
        if run_data["status"] != "SUCCEEDED":
            print (f"<==== Actor run failed: {run_data}")
            raise Exception(f"Actor gagal: {run_data['status']}")

        dataset_id = run_data["defaultDatasetId"]

        dataset_url = f"{BASE_URL}/datasets/{dataset_id}/items?clean=true&token={APIFY_TOKEN}"
        data_resp = requests.get(dataset_url)
        data_resp.raise_for_status()

        items: List[Dict[str, Any]] = data_resp.json()

        return items

    async def get_header_kol(self, db: AsyncSession, kol_account: str, latest_post: str = None, socmed_type: str = "") -> KOLHeader:
        # print("<===================Fetching header data for KOL account:", kol_account)
        #get data header
        data_result = await self.call_apify({
            "addParentData": False,
            "directUrls": [
                "https://www.instagram.com/" + kol_account + "/",
            ],
            "onlyPostsNewerThan": "90 days",
            "resultsLimit": 1,
            "resultsType": "details",
            "searchLimit": 1,
            "searchType": "hashtag"
        },
        actor_id="apify~instagram-scraper"
        )

        data_kol = data_result[0] if data_result else None
        if not data_kol:
            return None
        
        header_obj = KOLHeader(
            kol_account=kol_account,
            kol_name=data_kol.get("fullName"),
            bio=data_kol.get("biography"),
            bussiness_category=data_kol.get("businessCategoryName"),
            followers=data_kol.get("followersCount"),
            following=data_kol.get("followsCount"),
            profile_picture=data_kol.get("profilePicUrl"),
            last_update=datetime.utcnow(),
            last_post=latest_post,
            socmed_type=socmed_type
        )

        created = await kol_service.insertHeader(db, obj_in=header_obj)
        return header_obj

    async def get_detail_kol(self, db: AsyncSession, kol_account: str, socmed_type: str = "") -> KOLData:    
        items = await self.call_apify({
            "addParentData": False,
            "directUrls": [
                "https://www.instagram.com/" + kol_account + "/",
            ],
            "onlyPostsNewerThan": "90 days",
            "resultsLimit": 50,
            "resultsType": "posts",
            "searchLimit": 1,
            "searchType": "hashtag"
            },
            actor_id="apify~instagram-scraper"
        )

        day_ranges = [7, 30, 60, 90]
        results = []
        inserted_data = []

        now = datetime.now(timezone.utc)

        # =============================
        # 🔥 TOP 5 POST TERBARU
        # =============================
        valid_items = []

        for item in items:
            ts = item.get("timestamp")
            if not ts:
                continue

            post_date = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            valid_items.append((post_date, item))

        # sort by newest
        valid_items.sort(key=lambda x: x[0], reverse=True)

        top_posts = []
        for _, item in valid_items[:5]:
            top_posts.append({
                "url": item.get("displayUrl"),
                "like": item.get("likesCount", 0),
                "comment": item.get("commentsCount", 0)
            })
        top_posts_str = json.dumps(top_posts)

        header = await self.get_header_kol(db, kol_account=kol_account, latest_post=top_posts_str, socmed_type=socmed_type)

        for days in day_ranges:
            # print("<======== PROCESSING DAY : "+str(days)+"========>\n")
            cutoff = now - timedelta(days=days)
            filtered_items = []

            for item in items:
                ts = item.get("timestamp")
                if not ts:
                    continue

                post_date = datetime.fromisoformat(ts.replace("Z", "+00:00"))

                if post_date >= cutoff:
                    filtered_items.append(item)

            # =============================
            # AGGREGATION
            # =============================

            total_posts = len(filtered_items)
            total_likes = 0
            total_comments = 0
            total_views = 0
            total_views_brand = 0
            total_reach = 0
            total_watch_time = 0
            video_posts_count = 0
            video_posts_brand_count = 0

            for item in filtered_items:
                likes = item.get("likesCount", 0)
                comments = item.get("commentsCount", 0)
                views = item.get("videoViewCount", 0)
                play_count = item.get("videoPlayCount", 0)
                duration = item.get("videoDuration", 0)
                mentions = item.get("mentions", [])

                total_likes += likes
                total_comments += comments

                if views and views > 0:
                    total_views += views
                    total_reach += views
                    video_posts_count += 1
                    if mentions and len(mentions) > 0:
                        total_views_brand += views
                        video_posts_brand_count += 1

                if play_count and duration:
                    total_watch_time += (play_count * duration)

            # skip kalau tidak ada data (optional, lebih proper)
            if total_posts == 0:
                continue

            video_posts_count = video_posts_count if video_posts_count > 0 else 1

            avg_like = total_likes / total_posts
            avg_comment = total_comments / total_posts

            # avg_reach = (total_reach / total_posts) * 0.7
            avg_reach = total_views / total_posts
            
            avg_view = total_views / video_posts_count
            
            # er = ((avg_like + avg_comment) / avg_reach * 100) if avg_reach > 0 else 0
            er = ((total_likes + total_comments) / total_posts)/header.followers * 100 if header.followers > 0 else 0
            
            print(video_posts_count, "/", video_posts_brand_count)
            avg_watch_time = total_watch_time / video_posts_count if video_posts_count > 0 else 0
            avg_brand_view = total_views_brand / video_posts_brand_count if video_posts_brand_count > 0 else 0
            # =============================
            # 🔥 TOP HASHTAG & MENTION
            # =============================
            hashtag_counter = Counter()
            mention_counter = Counter()

            for item in filtered_items:
                hashtags = item.get("hashtags", []) or []
                tagged_users = item.get("taggedUsers", []) or []

                # print(hashtags, tagged_users)

                # hitung hashtag
                hashtag_counter.update([h.lower() for h in hashtags if h])

                # hitung mention (username)
                for user in tagged_users:
                    username = user.get("username")
                    if username:
                        mention_counter.update([username.lower()])
            top_hashtags = ",".join([h for h, _ in hashtag_counter.most_common(10)])
            top_mentions = ",".join([m for m, _ in mention_counter.most_common(5)])
        
            data_obj = {
                "kol_account": kol_account,
                "total_post": total_posts,
                "avg_like": avg_like,
                "avg_comment": avg_comment,
                "avg_reach": avg_reach,
                "avg_view": avg_view,
                "avg_brand_view": avg_brand_view,
                "er": er,
                "avg_watch_time": avg_watch_time,
                "last_update": datetime.utcnow(),
                "created_by": "SYSTEM",
                "created_dt": datetime.utcnow(),
                "days": str(days),
                "top_hashtags": top_hashtags,
                "top_mentions": top_mentions,
                "socmed_type": socmed_type
            }

            results.append(data_obj)
            created = await self.create(db, obj_in=data_obj)

        result_90_days = await self.get_detail_by_account(db, kol_account=kol_account, days="90", socmed_type=socmed_type)
        return KOLData(header=header, detail=result_90_days)

    async def get_kol_data(self, db: AsyncSession, kol_account: str, socmed_type: str) -> KOLData:
        header = await self.get_header_by_account(db, kol_account=kol_account, socmed_type=socmed_type)

        # =============================
        # 1. Kalau tidak ada data → fetch API
        # =============================
        if not header:
            print(f"<==== No data, fetching from API: {kol_account}")
            if socmed_type == "tiktok":
                return await self.get_data_kol_tiktok(db, kol_account=kol_account, socmed_type=socmed_type)
            else:
                return await self.get_detail_kol(db, kol_account=kol_account, socmed_type=socmed_type)


        # =============================
        # 2. Cek apakah data masih fresh
        # =============================
        now = datetime.now(timezone.utc)
        last_update = header.last_update

        # handle naive datetime
        if last_update and last_update.tzinfo is None:
            last_update = last_update.replace(tzinfo=timezone.utc)

        is_fresh = False

        refresh_threshold = await master_system_service.get_system_value(db=db, system_type="KOL_SETTINGS", system_cd="REFRESH_PERIOD")
        if last_update:
            diff_days = (now - last_update).days
            is_fresh = diff_days <= int(refresh_threshold)   # 🔥 <= 7 hari masih fresh


        # =============================
        # 3. Kalau fresh → ambil dari DB
        # =============================
        if is_fresh:
            detail = await self.get_detail_by_account(db, kol_account=kol_account, socmed_type=socmed_type)
            print(f"<==== Fetched fresh data for {kol_account}: {detail}")
            return KOLData(header=header, detail=detail)


        # =============================
        # 4. Kalau expired → refresh data
        # =============================
        print(f"<==== Data expired (>7 days), refreshing: {kol_account}")

        await self.delete_by_account(db, kol_account=kol_account, socmed_type=socmed_type)
        if socmed_type == "tiktok":
            data = await self.get_data_kol_tiktok(db, kol_account=kol_account, socmed_type=socmed_type)
        else:
            data = await self.get_detail_kol(db, kol_account=kol_account, socmed_type=socmed_type)

        print(f"<==== Data refreshed: {kol_account}")

        return data

    async def get_kol_list(
        self,
        db: AsyncSession,
        kol_account: str = "",
        min_avg_like: float = 0,
        max_avg_like: float = 0,
        min_followers: int = 0,
        max_followers: int = 0,
        hashtag: str = "",
        socmed_type: str = ""
    ) -> List[KOLSearch]:

        query = (
            select(
                KOLHeaderModel.kol_account,
                KOLHeaderModel.kol_name,
                KOLHeaderModel.profile_picture,
                KOLHeaderModel.followers,
                KOLDetailModel.total_post,
                KOLDetailModel.avg_view,
                KOLDetailModel.avg_brand_view,
                KOLDetailModel.er,
                KOLDetailModel.socmed_type
            )
            .join(
                KOLDetailModel,
                KOLHeaderModel.kol_account == KOLDetailModel.kol_account,
            )
            .where(KOLDetailModel.days == "90")  # 🔥 wajib biar tidak duplicate
        )

        conditions = []

        # =============================
        # FILTER kol_account
        # =============================
        if kol_account:
            conditions.append(KOLHeaderModel.kol_account.ilike(f"%{kol_account}%"))

        # =============================
        # FILTER followers
        # =============================
        if min_followers > 0:
            conditions.append(KOLHeaderModel.followers >= min_followers)

        if max_followers > 0:
            conditions.append(KOLHeaderModel.followers <= max_followers)

        # =============================
        # FILTER avg_like
        # =============================
        if min_avg_like > 0:
            conditions.append(KOLDetailModel.avg_like >= min_avg_like)

        if max_avg_like > 0:
            conditions.append(KOLDetailModel.avg_like <= max_avg_like)

        # =============================
        # FILTER hashtag
        # =============================
        if hashtag:
            conditions.append(KOLDetailModel.top_hashtags.ilike(f"%{hashtag.lower()}%"))
        
        # =============================
        # FILTER socmed_type
        # =============================
        if socmed_type.lower() != "all":
            conditions.append(KOLDetailModel.socmed_type == socmed_type)

        # =============================
        # APPLY FILTER
        # =============================
        for item in conditions:
            print(f"<==== Applying filter condition: {item}")

        if conditions:
            query = query.where(and_(*conditions))

        # =============================
        # ORDER
        # =============================
        query = query.order_by(KOLHeaderModel.last_update.desc())

        result = await db.execute(query)
        rows = result.all()

        # =============================
        # MAPPING
        # =============================
        data = []
        for i, row in enumerate(rows, start=1):
            data.append(KOLSearch(
                no=i,
                kol_account=row.kol_account,
                kol_name=row.kol_name,
                profile_picture=row.profile_picture,
                total_follower=row.followers,
                total_post=row.total_post,
                avg_view=row.avg_view,
                avg_brand_view=row.avg_brand_view,
                er=row.er
            ))
        return data
    
    async def get_data_post_instagram(
            self,
            post_url: str
        ) -> PostData:

        payload = { 
            "addParentData": False,
            "directUrls": [
                post_url
            ],
            "onlyPostsNewerThan": "90 days",
            "resultsLimit": 1,
        }

        data_result = await self.call_apify(payload, actor_id="apify~instagram-scraper")
        
        data_kol = data_result[0] if data_result else None
        if not data_kol:
            return None

        duration = data_kol.get("videoDuration", 0)
        play_count = data_kol.get("videoPlayCount", 0)

        factor = 0.4
        if duration <= 15:
            factor = 0.5
        elif duration <= 60:
            factor = 0.4
        else:
            factor = 0.3
        
        avg_watch_time = play_count * duration * factor
        str_avg_watch_time = self.formatWatchTime(int(avg_watch_time))
        
        return PostData(
            post_url=post_url,
            caption=data_kol.get("caption"),
            hashtags=data_kol.get("hashtags", []),
            taggedUsers=[u.get("username") for u in data_kol.get("taggedUsers", [])],
            likeCount=data_kol.get("likesCount", 0),
            commentCount=data_kol.get("commentsCount", 0),
            viewCount=data_kol.get("videoViewCount", 0),
            playCount=play_count,
            duration=duration,
            displayUrl=data_kol.get("displayUrl"),
            shareCount=0,
            repostCount=0,
            saveCount=0,
            avg_watch_time=str_avg_watch_time
        )

    async def get_data_kol_tiktok(
            self,
            db: AsyncSession,
            kol_account: str,
            socmed_type: str
        ) -> KOLData:

        data_result = await self.call_apify(
            {
                "commentsPerPost": 0,
                "excludePinnedPosts": False,
                "maxFollowersPerProfile": 0,
                "maxFollowingPerProfile": 0,
                "maxProfilesPerQuery": 1,
                "maxRepliesPerComment": 0,
                "oldestPostDateUnified": "90 days",
                "profileScrapeSections": [
                    "videos"
                ],
                "profileSorting": "latest",
                "profiles": [
                    "https://www.tiktok.com/@" + kol_account
                ],
                "proxyCountryCode": "None",
                "resultsPerPage": 50,
                "scrapeRelatedVideos": False,
                "shouldDownloadAvatars": False,
                "shouldDownloadCovers": False,
                "shouldDownloadMusicCovers": False,
                "shouldDownloadSlideshowImages": False,
                "shouldDownloadVideos": False,
                "topLevelCommentsPerPost": 0
            }, 
            actor_id="clockworks~tiktok-scraper"
        )
        
        data_kol_header = data_result[0] if data_result else None
        if not data_kol_header:
            return KOLData(
                header=None,
                detail=None
            )

        top_5_raw = sorted(
            data_result,
            key=lambda x: x.get("createTime", 0),
            reverse=True
        )[:5]

        top_5_posts = []

        for idx, item in enumerate(top_5_raw, start=1):
            original_url = item.get("videoMeta", {}).get("originalCoverUrl")

            uploaded_url = None

            if original_url:
                try:
                    uploaded_url = await self.upload_kol_image(image_url=original_url, foto_id=f"{kol_account}_post_{idx}")
                except Exception as e:
                    print(f"Upload failed for post {idx}: {e}")

            top_5_posts.append({
                "url": uploaded_url,  # 🔥 pakai hasil upload
                "like": item.get("diggCount", 0),
                "comment": item.get("commentCount", 0),
                "createTime": item.get("createTime", 0),
            })

        top_posts_str = json.dumps(top_5_posts).replace('\\', '"')

        original_url = data_kol_header.get("authorMeta", {}).get("avatar")
        display_url = None
        picture_id = kol_account + "_PP"
        if original_url:
            display_url = await self.upload_kol_image(image_url=original_url, foto_id=picture_id)

        data_obj =KOLHeader(
            kol_account=kol_account,
            kol_name=data_kol_header.get("authorMeta", {}).get("name"),
            bio=data_kol_header.get("authorMeta", {}).get("signature"),
            bussiness_category="",
            followers=data_kol_header.get("authorMeta", {}).get("fans"),
            following=data_kol_header.get("authorMeta", {}).get("following"),
            profile_picture=display_url,
            last_update=datetime.utcnow(),
            last_post=top_posts_str,
            socmed_type=socmed_type
        )
        created_header = await self.insertHeader(db, obj_in=data_obj)
        
        day_ranges = [7, 30, 60, 90]
        now = datetime.now(timezone.utc)
        for days in day_ranges:
            cutoff = now - timedelta(days=days)
            filtered_items = []

            for item in data_result:
                ts = item.get("createTimeISO")
                if not ts:
                    continue

                post_date = datetime.fromisoformat(ts.replace("Z", "+00:00"))

                if post_date >= cutoff:
                    filtered_items.append(item)

            # =============================
            # AGGREGATION
            # =============================

            total_posts = len(filtered_items)
            total_likes = 0
            total_comments = 0
            total_views = 0
            total_views_brand = 0
            total_reach = 0
            total_watch_time = 0
            video_posts_count = 0
            video_brand_posts_count = 0

            for item in filtered_items:
                likes = item.get("diggCount", 0)
                comments = item.get("commentCount", 0)
                views = item.get("playCount", 0)
                play_count = item.get("playCount", 0)
                duration = item.get("videoMeta", {}).get("duration", 0) if item.get("videoMeta") else 0
                mentions = item.get("detailedMentions", [])

                total_likes += likes
                total_comments += comments

                if views and views > 0:
                    total_views += views
                    total_reach += views
                    video_posts_count += 1
                    if mentions and len(mentions) > 0:
                        total_views_brand += views
                        video_brand_posts_count += 1

                if play_count and duration:
                    total_watch_time += (play_count * duration)

            # skip kalau tidak ada data (optional, lebih proper)
            if total_posts == 0:
                continue

            video_posts_count = video_posts_count if video_posts_count > 0 else 1

            avg_like = total_likes / total_posts
            avg_comment = total_comments / total_posts

            # avg_reach = (total_reach / total_posts) * 0.7
            avg_reach = total_views / total_posts
            
            avg_view = total_views / video_posts_count
            
            # er = ((avg_like + avg_comment) / avg_reach * 100) if avg_reach > 0 else 0
            er = ((total_likes + total_comments) / total_posts)/created_header.followers * 100 if created_header.followers > 0 else 0
            
            avg_watch_time = total_watch_time / video_posts_count
            avg_brand_view = total_views_brand / video_brand_posts_count if video_brand_posts_count > 0 else 0
            # =============================
            # 🔥 TOP HASHTAG & MENTION
            # =============================
            hashtag_counter = Counter()
            mention_counter = Counter()

            for item in filtered_items:
                hashtags = item.get("hashtags", []) or []
                tagged_users = item.get("taggedUsers", []) or []

                # print(hashtags, tagged_users)

                # hitung hashtag
                clean_hashtags = []
                for h in hashtags:
                    if isinstance(h, dict) and "name" in h:
                        clean_hashtags.append(h["name"].lower())
                    elif isinstance(h, str):
                        clean_hashtags.append(h.lower())

                hashtag_counter.update(clean_hashtags)
                # hitung mention (username)
                for user in tagged_users:
                    username = user.get("username")
                    if username:
                        mention_counter.update([username.lower()])

            top_hashtags = ",".join(h for h, _ in hashtag_counter.most_common(10) if h and h.strip())
            top_mentions = ",".join([m for m, _ in mention_counter.most_common(5)])
        
            data_detail = {
                "kol_account": kol_account,
                "total_post": total_posts,
                "avg_like": avg_like,
                "avg_comment": avg_comment,
                "avg_reach": avg_reach,
                "avg_view": avg_view,
                "avg_brand_view": avg_brand_view,
                "er": er,
                "avg_watch_time": avg_watch_time,
                "last_update": datetime.utcnow(),
                "created_by": "SYSTEM",
                "created_dt": datetime.utcnow(),
                "days": str(days),
                "top_hashtags": top_hashtags,
                "top_mentions": top_mentions,
                "socmed_type": socmed_type
            }
            created_detail = await self.create(db, obj_in=data_detail)

        result_90_days = await self.get_detail_by_account(db, kol_account=kol_account, days="90", socmed_type=socmed_type)
        return KOLData(
            header=created_header,
            detail=result_90_days
        )
    
    async def get_data_post_tiktok(
            self,
            post_url: str
        ) -> PostData:

        data_result = await self.call_apify(
            {
                "commentsPerPost": 0,
                "excludePinnedPosts": False,
                "maxFollowersPerProfile": 0,
                "maxFollowingPerProfile": 0,
                "maxProfilesPerQuery": 1,
                "maxRepliesPerComment": 0,
                "postURLs": [
                    post_url
                ],
                "proxyCountryCode": "None",
                "resultsPerPage": 1,
                "scrapeRelatedVideos": False,
                "shouldDownloadAvatars": False,
                "shouldDownloadCovers": False,
                "shouldDownloadMusicCovers": False,
                "shouldDownloadSlideshowImages": False,
                "shouldDownloadVideos": False,
                "topLevelCommentsPerPost": 0
            }, 
            actor_id="clockworks~tiktok-scraper"
        )
        
        data_kol = data_result[0] if data_result else None
        if not data_kol:
            return None
        
        video_meta = data_kol.get("videoMeta") or {}
        duration = video_meta.get("duration", 0)
        play_count = data_kol.get("playCount", 0)

        factor = 0.4  # default factor
        if duration <= 15:
            factor = 0.5
        elif duration <= 60:
            factor = 0.4
        else:
            factor = 0.3
        
        avg_watch_time = play_count * duration * factor
        str_avg_watch_time = self.formatWatchTime(int(avg_watch_time))

        return PostData(
            post_url=post_url,
            caption=data_kol.get("text"),

            hashtags=[
                h.get("name").strip()
                for h in data_kol.get("hashtags", [])
                if isinstance(h, dict)
                and h.get("name")
                and h.get("name").strip()
            ],
            taggedUsers=[
                m.get("nickName").strip()
                for m in data_kol.get("detailedMentions", [])
                if isinstance(m, dict)
                and m.get("nickName")
                and m.get("nickName").strip()
            ],
            likeCount=data_kol.get("diggCount", 0),
            commentCount=data_kol.get("commentCount", 0),
            viewCount=play_count,
            playCount=play_count,

            duration=duration,

            displayUrl=(
                video_meta.get("originalCoverUrl")
                or video_meta.get("coverUrl")
            ),
            shareCount=data_kol.get("shareCount", 0),
            repostCount=data_kol.get("repostCount", 0),
            saveCount=data_kol.get("collectCount", 0),
            avg_watch_time=str_avg_watch_time
        )
    
    async def get_post_url(self, db: AsyncSession, id: str) -> Report | None:
        int_id = int(id)
        result = await db.execute(
                select(Report.link).where(
                    Report.id == int_id
                )
            )
        return result.scalars().first()
    
    async def get_data_post(self, db: AsyncSession, id: str) -> PostData:
        print(f"<==== Fetching post data for report ID: {id}")
        post_url = await self.get_post_url(db, id=id)
        if not post_url:
            raise ValueError("Report not found")
        
        print(f"<==== Fetching post data for URL: {post_url}")
        
        socmed_type = ""
        if "tiktok.com" in post_url:
            socmed_type = "tiktok"
        elif "instagram.com" in post_url:
            socmed_type = "instagram"

        print(post_url)

        if socmed_type.lower() == "tiktok":
            return await self.get_data_post_tiktok(post_url=post_url)
        elif socmed_type.lower() == "instagram":
            return await self.get_data_post_instagram(post_url=post_url)
        else:
            raise ValueError("Unsupported social media type")
        
    async def upload_kol_image(self, image_url: str, foto_id: str) -> str | None:
        try:
            result = cloudinary.uploader.upload(
                image_url,
                public_id=f"kol/{foto_id}",  # 🔥 custom nama
                overwrite=True,                 # 🔥 replace file lama
                resource_type="image"
            )
            return result.get("secure_url")
        except Exception as e:
            print("Upload failed:", e)
            return None
    
    def formatWatchTime(self, seconds: int) -> str:
        if seconds < 60:
            return f"{seconds} Detik"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} Menit"
        else:
            hours = seconds // 3600
            return f"{hours} Jam"
        
kol_service = KOLService()
