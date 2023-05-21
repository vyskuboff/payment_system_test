from aiogram.fsm.state import State, StatesGroup


class SendMoneyState(StatesGroup):
    waiting_for_phone_input = State()
    waiting_for_money_input = State()


class RegistrationState(StatesGroup):
    waiting_for_phone_input = State()