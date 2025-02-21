import asyncio
import logging
from sqlalchemy import select
from database.create_db import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def add_user(user_id: int, username: str, referral_code: str) -> Boolean:
    try:
        async with async_session() as session:
            async with session.begin():
                new_user = User(user_id=user_id,
                                username=username,
                                referral_code=referral_code)  
                
                session.add(new_user)
        return True
    
    except Exception as e:
        logging.info(f"Ошибка при добавлении пользователя (user_id={user_id}, username='{username}'): {e}")
        return False
    
async def is_exists_user(user_id: int) -> Boolean:
    try:
        async with async_session() as sessio:
            result = await sessio.execute(select(User).where(User.user_id == user_id))
            return result.scalar_one_or_none() is not None
    except Exception as e:
        logging.info(f"Ошибка при проверке наличия пользователя (user_id={user_id}): {e}")
        return False
