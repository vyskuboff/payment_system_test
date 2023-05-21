import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import postgres_url, telegram_token
from db import create_async_engine, get_session_maker
from dictionary import bot_commands
from handlers import register_user_commands
from middleware import RegisterCheck


async def bot_start(logger: logging.Logger) -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    bot = Bot(token=telegram_token)

    await bot.set_my_commands(commands=commands_for_bot)
    register_user_commands(dp)

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await dp.start_polling(bot, logger=logger, session_maker=session_maker)


def main():
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(bot_start(logger))
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')


if __name__ == '__main__':
    main()