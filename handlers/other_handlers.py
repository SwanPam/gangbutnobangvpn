from aiogram import Router, types

other_router = Router()

@other_router.message()
async def echo(message: types.Message):
    await message.answer(f"Вы сказали: {message.text}")