import re
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.device_rq import *
from keyboards.devices_kb import my_devices_menu_keyboard

devices_router = Router()

class DeviceAddState(StatesGroup):
    name = State()
    
@devices_router.message(Command('my_devices'))
@devices_router.callback_query(F.data == 'my_devices')
async def my_devices(update: CallbackQuery):
    user_id = update.from_user.id
    devices = await get_my_devices(user_id)
    keyboard = my_devices_menu_keyboard(devices, 'select')
    if isinstance(update, CallbackQuery):
        await update.message.answer("Мои устройства", reply_markup=keyboard)
        await update.answer('')
    elif isinstance(update, Message):
        await update.answer("Мои устройства", reply_markup=keyboard)

@devices_router.callback_query(F.data == 'add_device')
async def add_device(update: CallbackQuery, state: FSMContext):
    await update.answer()
    await update.message.answer("Введите имя устройства:")
    await state.set_state(DeviceAddState.name)
    
@devices_router.message(DeviceAddState.name)
async def enter_device_name(message: Message, state: FSMContext):
    device_name = message.text
    user_id = message.from_user.id
    await create_device_in_db(user_id, device_name)
    await message.answer(f"Устройство '{device_name}' успешно добавлено для юзера {user_id}.")
    await state.clear()

class DeviceRemoveState(StatesGroup):
    confirmation = State()
    
@devices_router.callback_query(F.data == 'remove_device')
async def remove(update: CallbackQuery):
    user_id = update.from_user.id
    devices = await get_my_devices(user_id)
    keyboard = my_devices_menu_keyboard(devices, 'remove')
    await update.message.answer("Выберите устройство для удаления", reply_markup=keyboard)
    await update.answer('')
    
@devices_router.callback_query(F.data.func(lambda data: re.match(r"^device_.*_remove$", data)))
async def remove(update: CallbackQuery, state: FSMContext):
    device_id = int(update.data.split('_')[1])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подтвердить', callback_data='confirm_device_remove')],
        [InlineKeyboardButton(text='Отмена', callback_data='cancel_device_remove')]
        ])
    await update.message.answer("Подтвердите удаление устройства", reply_markup=keyboard)
    await update.answer('')
    await state.update_data(device_id = device_id)
    
@devices_router.callback_query(F.data == 'confirm_device_remove')
async def remove(update: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if await remove_device(data["device_id"]):
        text = 'Устройство успешно удалено'
    else:
        text = 'Ошибка удаления устройства'
    await update.message.answer(text)
    await update.answer('')
    await state.clear()

@devices_router.callback_query(F.data == 'cancel_device_remove')
async def remove(update: CallbackQuery, state: FSMContext):
    text = 'Удаление устройства отменено'
    await update.message.answer(text)
    await update.answer('')
    await state.clear()