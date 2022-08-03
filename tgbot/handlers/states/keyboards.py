from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ReplyMarkup, WebAppInfo

from tgbot.handlers.states.static_text import language_codes, MAN, WOMAN, BOYS, GIRLS, ALL, SEND_LOCATION, ENOUGH_PHOTO, \
    BACK, SKIP, CHANGE_MAIN, EDIT_PROFILE, SAVE_CURRENT, REMOVE_ALL_PHOTO, SAVE_CURRENT_DESC, WATCH_PROFILE
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

    if user.name is not None and user.first_name != user.name:
        buttons[0].append(KeyboardButton(user.name))

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_interest(lan) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(BOYS[lan]), KeyboardButton(GIRLS[lan]), KeyboardButton(ALL[lan])
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_location_keyboard(lan, exists=False) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(SEND_LOCATION[lan], request_location=True)
        ]
    ]

    if exists:
        buttons[0].append(KeyboardButton(SAVE_CURRENT[lan]))

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
        buttons[0].append(KeyboardButton(REMOVE_ALL_PHOTO[lan]))

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_description(lan, exists=False) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(SKIP[lan]), KeyboardButton(BACK[lan])
        ]
    ]

    if exists:
        buttons.append([
            KeyboardButton(SAVE_CURRENT_DESC[lan])
        ])

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_profile(user: User) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(CHANGE_MAIN[user.bot_language]), KeyboardButton(EDIT_PROFILE[user.bot_language]),

        ],
        [
            KeyboardButton(WATCH_PROFILE[user.bot_language], web_app=WebAppInfo('https://fresh-moth-37.loca.lt/'))
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def make_keyboard_for_age(user: User) -> ReplyMarkup:
    if user.age == 0:
        return ReplyKeyboardRemove()

    buttons = [
        [
            KeyboardButton(str(user.age))
        ]
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
