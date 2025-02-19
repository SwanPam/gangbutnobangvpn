from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.main_menu import main_menu_keyboard

start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(update: Message | CallbackQuery):
    keyboard = main_menu_keyboard()
    if isinstance(update, CallbackQuery):
        await update.message.answer("Привет! Я ваш Telegram-бот 🤖", reply_markup=keyboard)
        await update.answer('')
    elif isinstance(update, Message):
        await update.answer("Привет! Я ваш Telegram-бот 🤖", reply_markup=keyboard)