from aiogram.types import Update
from aiogram.dispatcher.middlewares.base import BaseMiddleware
import logging

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: Update):
        logging.info(f"Обновление: {update}")