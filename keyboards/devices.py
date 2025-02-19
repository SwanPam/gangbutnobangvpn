import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

def my_devices_menu_keyboard(devices: list = []):
    keyboard = InlineKeyboardBuilder()
    devices = devices or []

    test_devices = [
        {'id': 1, 'name': 'Device 1'},
        {'id': 2, 'name': 'Device 2'},
        {'id': 3, 'name': 'Device 3'}
    ]
    
    devices = test_devices if not devices else devices
    if not devices:
        logging.info("No devices found")
    else:
        for device in devices:
            keyboard.row(InlineKeyboardButton(text=device['name'], 
                                            callback_data=f"device_{device['id']}"))

    keyboard.row(InlineKeyboardButton(text="Добавить устройство", callback_data="add_device"),
                 InlineKeyboardButton(text="Удалить устройство", callback_data="remove_device"))
    keyboard.row(InlineKeyboardButton(text="Помощь", callback_data="help"))
    keyboard.row(InlineKeyboardButton(text="Главное меню", callback_data="main_menu"))
    
    return keyboard.as_markup()
