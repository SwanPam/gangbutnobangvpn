import asyncio

from sqlalchemy import select
from create_db import *

async def get_users():
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == 1))
        return result

if __name__ == '__main__':
    asyncio.run(get_users())
        