from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.states.keyboards import make_keyboard_for_sex, make_keyboard_for_language, make_keyboard_for_name, \
    make_keyboard_for_interest
from tgbot.handlers.states.static_text import language_codes, CHOOSE_SEX, CHOOSE_LANGUAGE, MAN, WOMAN, ENTER_AGE, \
    ENTER_NAME, CHOOSE_INTEREST, BOYS, GIRLS, ALL
from tgbot.models import User

LANGUAGE, SEX, AGE, NAME, LOCATION, INTEREST = range(6)


def choose_language(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    if update.message.text in language_codes:
        u.bot_language = language_codes[update.message.text]
        u.save()

        update.message.reply_text(
            CHOOSE_SEX[u.bot_language],
            reply_markup=make_keyboard_for_sex(u.bot_language)
        )

        return SEX
    else:
        update.message.reply_text(
            CHOOSE_LANGUAGE[u.bot_language],
            reply_markup=make_keyboard_for_language()
        )

        return LANGUAGE


def choose_sex(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    if update.message.text in [MAN[u.bot_language], WOMAN[u.bot_language]]:
        if update.message.text == MAN[u.bot_language]:
            u.sex = User.Sex.MALE
        else:
            u.sex = User.Sex.FEMALE

        u.save()

        update.message.reply_text(
            ENTER_AGE[u.bot_language],
            reply_markup=ReplyKeyboardRemove()
        )

        return AGE
    else:
        update.message.reply_text(
            CHOOSE_SEX[u.bot_language],
            reply_markup=make_keyboard_for_sex(u.bot_language)
        )

        return SEX


def set_age(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    msg = update.message.text

    if msg.isdigit() and 16 <= int(msg) < 30:
        u.age = int(msg)
        u.save()

        update.message.reply_text(
            ENTER_NAME[u.bot_language],
            reply_markup=make_keyboard_for_name(u)
        )

        return NAME

    else:
        update.message.reply_text(
            ENTER_AGE[u.bot_language]
        )

        return AGE


def set_name(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    name = update.message.text[:30]
    u.name = name

    update.message.reply_text(
        CHOOSE_INTEREST[u.bot_language],
        reply_markup=make_keyboard_for_interest(u.bot_language)
    )

    return INTEREST


def set_interest(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    if update.message.text in [BOYS[u.bot_language], GIRLS[u.bot_language], ALL[u.bot_language]]:
        if update.message.text == BOYS[u.bot_language]:
            u.interested_in = User.Interest.BOYS
        elif update.message.text == GIRLS[u.bot_language]:
            u.interested_in = User.Interest.GIRLS
        else:
            u.interested_in = User.Interest.ALL

        u.save()

        update.message.reply_text(
            "ABOBUS",
            reply_markup=ReplyKeyboardRemove()
        )

        return LOCATION
    else:
        update.message.reply_text(
            CHOOSE_INTEREST[u.bot_language],
            reply_markup=make_keyboard_for_interest(u.bot_language)
        )

        return INTEREST
