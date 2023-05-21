from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from config import LIMIT
from context import get_user
from keyboards import main_menu_keyboard
from state import SendMoneyState
from handlers.utils import send_need_to_enter_phone


async def get_balance(call, session_maker: sessionmaker, state: FSMContext):
    user = await get_user(call.from_user.id, session_maker)
    if not user.phone:
        return await send_need_to_enter_phone(call.message, state)

    return await call.message.answer(
        f'Баланс: {user.balance} \nЛимит: {LIMIT}\nВыберите действие',
        reply_markup=main_menu_keyboard()
    )


async def request_phone_input(call, session_maker: sessionmaker, state: FSMContext):
    user = await get_user(call.from_user.id, session_maker)
    if not user.phone:
        return await send_need_to_enter_phone(call.message, state)
    await state.set_state(SendMoneyState.waiting_for_phone_input)
    return await call.message.answer(
        f'Введите номер телефона получателя'
    )
