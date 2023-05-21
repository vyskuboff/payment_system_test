from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def error_handler(message: types.Message, state: FSMContext) -> Message:

    return await message.answer('Ошибка при выполнении команды')
