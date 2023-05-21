from state import RegistrationState
from keyboards import send_contact_keyboard


async def send_need_to_enter_phone(message, state):
    await state.set_state(RegistrationState.waiting_for_phone_input)
    return await message.answer('Для регистрации в боте необходимо отправить свой номер телефона.',
                                reply_markup=send_contact_keyboard())