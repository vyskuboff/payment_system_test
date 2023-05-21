from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.button(
        text='Баланс',
        callback_data='get_balance')

    menu_builder.button(
        text='Сделать перевод',
        callback_data='send_money')

    return menu_builder.as_markup()