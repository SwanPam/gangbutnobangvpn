from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.main_menu_kb import main_menu_keyboard
from database import user_req
import utils
start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(update: Message | CallbackQuery):
    user_id, username = update.from_user.id, update.from_user.username
    if await user_req.is_exists_user(user_id):
        text=f'''Привет, {username}!
        '''
    else:
        referral_code = await utils.generate_referral_code(user_id)
        
        if await user_req.add_user(user_id, username, referral_code):
            text_susseced_reg = f'''Вы успешно зарегистрировались! id={user_id} username={username}'''
            text=f'''Добро пожаловать, {username}!
            '''
            await update.answer(text=text_susseced_reg)
        else:
            text=f'''Ошибка регистрации. Повторите попытку, введя /start.
            '''
            
    keyboard = main_menu_keyboard()
    if isinstance(update, CallbackQuery):
        await update.message.answer(text=text, reply_markup=keyboard)
        await update.answer('')
    elif isinstance(update, Message):
        await update.answer(text=text, reply_markup=keyboard)