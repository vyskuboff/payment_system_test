from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from context import get_user
from keyboards import main_menu_keyboard
from handlers.utils import send_need_to_enter_phone


async def start_handler(message: types.Message, session_maker: sessionmaker, state: FSMContext) -> Message:
    user = await get_user(message.from_user.id, session_maker)
    if not user:
        await send_need_to_enter_phone(message, state)

    elif not user.phone:
        await send_need_to_enter_phone(message, state)

    else:
        return await message.answer('Выберите действие', reply_markup=main_menu_keyboard())





