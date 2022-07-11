from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ReplyMarkup

from tgbot.handlers.states.static_text import language_codes, MAN, WOMAN, BOYS, GIRLS, ALL, SEND_LOCATION, ENOUGH_PHOTO, \
    BACK
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


def make_location_keyboard(lan) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(SEND_LOCATION[lan], request_location=True)
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_select_location_keyboard(names) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(name)
        ] for name in names
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_photo(lan, first=False) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(BACK[lan])
        ]
    ]

    if not first:
        buttons[0].append(KeyboardButton(ENOUGH_PHOTO[lan]))

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
