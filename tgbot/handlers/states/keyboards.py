from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ReplyMarkup

from tgbot.handlers.states.static_text import language_codes, MAN, WOMAN, BOYS, GIRLS, ALL
from tgbot.models import User


def make_keyboard_for_language() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(lan) for lan in language_codes.keys()
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_sex(lan) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(MAN[lan]), KeyboardButton(WOMAN[lan])
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_name(user: User) -> ReplyMarkup:
    if user.first_name is None or user.first_name == "":
        return ReplyKeyboardRemove()

    buttons = [
        [
            KeyboardButton(user.first_name)
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_interest(lan) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(BOYS[lan]), KeyboardButton(GIRLS[lan]), KeyboardButton(ALL[lan])
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
