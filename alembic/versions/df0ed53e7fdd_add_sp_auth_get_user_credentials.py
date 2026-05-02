"""add_sp_auth_get_user_credentials

Revision ID: df0ed53e7fdd
Revises: f809cde4b132
Create Date: 2026-01-14 05:33:15.237731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df0ed53e7fdd'
down_revision: Union[str, None] = 'f809cde4b132'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION sp_auth_get_user_credentials(
        -- Input Parameter
        p_identifier VARCHAR, 
        
        -- Output Parameters
        OUT o_user_id BIGINT,
        OUT o_password_hash VARCHAR,
        OUT o_role_nm VARCHAR,
        OUT o_fullname VARCHAR,
        OUT o_is_active BOOLEAN,
        OUT o_email VARCHAR,
        OUT o_phone VARCHAR,
        OUT o_status_code VARCHAR,   
        OUT o_status_message VARCHAR 
    ) 
    RETURNS RECORD 
    LANGUAGE plpgsql
    SECURITY DEFINER 
    AS $$
    DECLARE
        v_identifier_clean VARCHAR;
    BEGIN
        -- 1. Sanitasi Input (Lowercase & Trim)
        v_identifier_clean := LOWER(TRIM(p_identifier));

        -- 2. Query Utama (Sekarang lebih direct ke tb_m_user)
        SELECT 
            u.user_id,
            u.password,
            r.role_nm,
            u.fullname,
            u.is_active,
            u.email,
            u.phone
        INTO 
            o_user_id,
            o_password_hash,
            o_role_nm,
            o_fullname,
            o_is_active,
            o_email,
            o_phone
        FROM 
            tb_m_user u
        INNER JOIN 
            tb_m_role r ON u.role_id = r.role_id
        WHERE 
            LOWER(u.username) = v_identifier_clean 
            OR LOWER(u.email) = v_identifier_clean 
            OR u.phone = v_identifier_clean 
        LIMIT 1;

        -- 3. Validasi Hasil Pencarian
        IF FOUND THEN
            o_status_code := '200';
            o_status_message := 'User found';
        ELSE
            -- Return nilai kosong yang aman
            o_user_id := NULL;
            o_password_hash := NULL;
            o_role_nm := NULL;
            o_fullname := NULL;
            o_is_active := FALSE;
            o_email := NULL;
            o_phone := NULL;
            o_status_code := '404';
            o_status_message := 'User identity not found';
        END IF;

    -- 4. Error Handling
    EXCEPTION WHEN OTHERS THEN
        o_user_id := NULL;
        o_status_code := '500';
        o_status_message := 'Database Error: ' || SQLSTATE; 
    END;
    $$;
    """)

def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS sp_auth_get_user_credentials(VARCHAR)")
