import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

def my_devices_menu_keyboard(devices: list = [], type: str = 'select'):
    keyboard = InlineKeyboardBuilder()
    devices = devices or []

    if not devices:
        logging.info("No devices found")
    else:
        for device in devices:
            keyboard.row(InlineKeyboardButton(text=device.name, 
                                            callback_data=f"device_{device.id}_{type}"))
    if type == 'remove':
        pass
    elif type == 'select':
        keyboard.row(InlineKeyboardButton(text="Добавить устройство", callback_data="add_device"),
                    InlineKeyboardButton(text="Удалить устройство", callback_data="remove_device"))
        keyboard.row(InlineKeyboardButton(text="Помощь", callback_data="help"))
        keyboard.row(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    
    return keyboard.as_markup()

def device_keyboard(device_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='Изменить имя', callback_data=f'rename_device_{device_id}'))
    keyboard.row(InlineKeyboardButton(text='Включить/отключить', callback_data=f'Enable/Disable'))
    keyboard.row(InlineKeyboardButton(text='Мои устройства', callback_data=f'my_devices'))
    keyboard.row(InlineKeyboardButton(text='Главное меню', callback_data=f'start'))
    return keyboard.as_markup()