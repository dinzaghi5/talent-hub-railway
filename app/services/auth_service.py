from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.security import verify_password
from app.models.user import User

class AuthService:
    async def authenticate(self, db: AsyncSession, identifier: str, password: str):
        # Call the Stored Procedure
        query = text("SELECT * FROM sp_auth_get_user_credentials(:identifier)")
        result = await db.execute(query, {"identifier": identifier})
        user_record = result.mappings().first()

        if not user_record:
            return None
        
        status_code = user_record.get('o_status_code')
        
        if status_code != '200':
            return None

        # Verify password
        hashed_password = user_record.get('o_password_hash')
        if not verify_password(password, hashed_password):
            return None
            
        return user_record

auth_service = AuthService()
