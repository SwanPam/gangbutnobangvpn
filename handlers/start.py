from aiogram import Router, types
from aiogram.filters import CommandStart

start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я ваш Telegram-бот 🤖")