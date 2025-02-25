import asyncio
import logging
from sqlalchemy import delete, select
from database.create_db import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def create_device_in_db(user_id: str, device_name: str) -> bool:
    async with async_session() as session:
        try:
            async with session.begin():
                new_key = VPNKey(key='testkey')
                session.add(new_key)
                await session.flush()
                
                new_device = Device(user_id = user_id,
                                    name = device_name,
                                    key_id=new_key.key_id)
                session.add(new_device)
            return True
        except Exception as e:
            print(f"Ошибка при добавлении устройства: {e}")
            return False
        
async def get_my_devices(user_id: int) -> list:
    async with async_session() as session:
        result = await session.execute(select(Device).where(Device.user_id==user_id))
        return result.scalars().all()
    
async def remove_device(device_id: int) -> bool:
    async with async_session() as session:
        try:
            async with session.begin():
                await session.execute(delete(Device).where(Device.id == device_id))
            return True
        except Exception as e:
            print(f"Ошибка при удалении устройства: {e}")
            return False
        