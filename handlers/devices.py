from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from keyboards.devices import my_devices_menu_keyboard

devices_router = Router()

@devices_router.message(Command('my_devices'))
@devices_router.callback_query(F.data == 'my_devices')
async def my_devices(update: CallbackQuery):
    keyboard = my_devices_menu_keyboard()
    if isinstance(update, CallbackQuery):
        await update.message.answer("Мои устройства", reply_markup=keyboard)
        await update.answer('')
    elif isinstance(update, Message):
        await update.answer("Мои устройства", reply_markup=keyboard)
