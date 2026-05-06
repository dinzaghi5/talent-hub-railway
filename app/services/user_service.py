from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserService:
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def check_role_exists(self, db: AsyncSession, role_id: int) -> bool:
        result = await db.execute(select(Role).filter(Role.role_id == role_id))
        return result.scalars().first() is not None

    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            password=hashed_password,
            fullname=user_in.fullname,
            role_id=user_in.role_id,
            phone=user_in.phone,
            created_by="SYSTEM"
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).filter(User.user_id == user_id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    async def update(self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, user_id: int) -> User | None:
        obj = await self.get(db, user_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

user_service = UserService()
