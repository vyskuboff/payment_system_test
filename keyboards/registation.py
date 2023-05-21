from aiogram.utils.keyboard import ReplyKeyboardBuilder


def send_contact_keyboard():
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text='Отправить контакт', request_contact=True)

    return menu_builder.as_markup()
