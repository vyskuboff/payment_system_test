from aiogram import Bot
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from config import LIMIT, telegram_token, logger
from context import create_transaction, get_user, get_user_by, update_user
from keyboards import main_menu_keyboard
from state import SendMoneyState
from handlers.utils import send_need_to_enter_phone

bot = Bot(token=telegram_token)


async def get_phone(message, session_maker: sessionmaker, state: FSMContext):
    if not message.contact:
        return await send_need_to_enter_phone(message, state)

    await update_user(message.from_user.id, session_maker, **{'phone': message.contact.phone_number, 'balance': 0})
    await state.clear()
    return await message.answer('Вы успешно зарегистрировались! Выберите действие', reply_markup=main_menu_keyboard())


async def request_money_input(message, session_maker, state: FSMContext):
    if not await get_user_by(session_maker, **{'phone': message.text}):
        return await message.answer(
            f'Данный номер не существует\nВведите номер телефона получателя'
        )

    await state.update_data(phone=message.text)
    await state.set_state(SendMoneyState.waiting_for_money_input)
    return await message.answer(
        f'Введите сумму перевода'
    )


async def transfer_money(message, session_maker, state: FSMContext):
    user = await get_user(message.from_user.id, session_maker)
    try:
        money = float(message.text)
    except ValueError:
        return await message.answer(f'Введите корректную сумму перевода')

    if money <= 0:
        return await message.answer(f'Введите корректную сумму перевода')

    if user.balance + LIMIT - money >= 0:
        data = await state.get_data()

        if not 'phone' in data:
            return await send_error(state, message)

        user_to = await get_user_by(session_maker, **{'phone': data['phone']})

        if user.phone == user_to.phone:
            return await send_error(state, message)

        await create_transaction(
            user_to=user_to.user_id,
            user_from=user.user_id,
            amount=money,
            session_maker=session_maker
        )
        await update_user(user.user_id, session_maker, **{'balance': user.balance - money})
        await update_user(user_to.user_id, session_maker, **{'balance': user_to.balance + money})

        logger.info(f'from user {user.phone} send to user {user_to.phone} amount: {money}')

        await state.clear()
        await bot.send_message(user_to.user_id, f'На Ваш счет поступило {money} от {user.phone}.')

        return await message.answer(
            f'Перевод выполнен\nВыберите действие', reply_markup=main_menu_keyboard()
        )

    return await message.answer(
        f'Недостаточно денег. \nВведите другую сумму перевода'

    )


async def send_error(state, message):
    await state.clear()
    return await message.answer(
        f'Ошибка при выполнении платежа\nВыберите действие', reply_markup=main_menu_keyboard()
    )
