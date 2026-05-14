from telegram import KeyboardButton, ReplyKeyboardMarkup


BUTTON_REGISTER = "Зарегистрироваться"
BUTTON_APPOINTMENT = "Записаться на приём"
BUTTON_INFO = "Информация"
BUTTON_CONTACTS = "Контакты"


def build_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [BUTTON_REGISTER, BUTTON_APPOINTMENT],
            [BUTTON_INFO, BUTTON_CONTACTS],
        ],
        resize_keyboard=True,
    )


def build_phone_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Поделиться контактом", request_contact=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
