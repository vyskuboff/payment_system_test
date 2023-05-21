from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state

from state import RegistrationState, SendMoneyState

from .callbacks import get_balance, request_phone_input
from .commands import error_handler, start_handler
from .common_handlers import get_phone, request_money_input, transfer_money

__all__ = ('register_user_commands', 'register_user_handlers')


def register_user_commands(router: Router) -> None:

    router.message.register(start_handler, CommandStart())
    router.message.register(start_handler, Command(commands=['registration']))

    router.message.register(request_money_input,  SendMoneyState.waiting_for_phone_input)
    router.message.register(transfer_money, SendMoneyState.waiting_for_money_input)
    router.message.register(get_phone, RegistrationState.waiting_for_phone_input)

    router.callback_query.register(get_balance, F.data == 'get_balance', any_state)
    router.callback_query.register(request_phone_input, F.data == 'send_money', any_state)


    router.callback_query.register(error_handler, any_state)


register_user_handlers = register_user_commands
