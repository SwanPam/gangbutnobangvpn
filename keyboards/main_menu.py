from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Мои устройства', callback_data='my_devices')],
            [InlineKeyboardButton(text='Реферальная система', callback_data='referral_system')],
            [InlineKeyboardButton(text='Баланс', callback_data='balance')],
            [InlineKeyboardButton(text='Помощь', callback_data='help')],
        ]
    )
    