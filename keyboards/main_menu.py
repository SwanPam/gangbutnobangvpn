from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Команда 1"), KeyboardButton(text="Команда 2")]
        ],
        resize_keyboard=True
    )