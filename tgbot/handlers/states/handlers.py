from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.states.keyboards import make_keyboard_for_sex, make_keyboard_for_language, make_keyboard_for_name, \
    make_keyboard_for_interest, make_location_keyboard, make_select_location_keyboard, make_keyboard_for_photo
from tgbot.handlers.states.static_text import language_codes, CHOOSE_SEX, CHOOSE_LANGUAGE, MAN, WOMAN, ENTER_AGE, \
    ENTER_NAME, CHOOSE_INTEREST, BOYS, GIRLS, ALL, ENTER_LOCATION, NOT_FOUND_LOCATION, SElECT_LOCATION, SEND_PHOTO, \
    BACK, ENOUGH_PHOTO
from tgbot.locations.utils import search_place
from tgbot.models import User, Media

LANGUAGE, SEX, AGE, NAME, LOCATION, INTEREST, SELECT_LOCATION, PHOTO, PROFILE = range(9)


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
            ENTER_LOCATION[u.bot_language],
            reply_markup=make_location_keyboard(u.bot_language)
        )

        return LOCATION
    else:
        update.message.reply_text(
            CHOOSE_INTEREST[u.bot_language],
            reply_markup=make_keyboard_for_interest(u.bot_language)
        )

        return INTEREST


def search_location(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    results = search_place(update.message.text)

    if len(results):

        context.user_data['location_candidates'] = results

        update.message.reply_text(
            SElECT_LOCATION[u.bot_language],
            reply_markup=make_select_location_keyboard(f"{obj['name']} ({obj['formatted_address']})" for obj in results)
        )

        return SELECT_LOCATION
    else:
        update.message.reply_text(
            NOT_FOUND_LOCATION[u.bot_language],
            reply_markup=make_location_keyboard(u.bot_language)
        )

        return LOCATION


def select_location(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    for candidate in context.user_data['location_candidates']:
        if f"{candidate['name']} ({candidate['formatted_address']})" == update.message.text:
            u.location_lat = candidate['geometry']['location']['lat']
            u.location_lon = candidate['geometry']['location']['lng']
            u.location_name = update.message.text
            u.save()

            u.media.all().delete()

            update.message.reply_text(
                photo_text(u),
                reply_markup=make_keyboard_for_photo(u.bot_language)
            )

            return PHOTO

    update.message.reply_text(
        SElECT_LOCATION[u.bot_language],
        reply_markup=make_select_location_keyboard(
            f"{obj['name']} ({obj['formatted_address']})" for obj in context.user_data['location_candidates'])
    )

    return SELECT_LOCATION


def photo_text(user: User):
    photo_count = user.media.filter(media_type=Media.MediaType.PHOTO).count()
    video_count = user.media.filter(media_type=Media.MediaType.VIDEO).count()

    return SEND_PHOTO[user.bot_language] % (photo_count, video_count)


def save_location(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    lat, lon = update.message.location.latitude, update.message.location.longitude

    u.location_lon = lon
    u.location_lat = lat
    u.location_name = "-"
    u.save()

    u.media.all().delete()

    update.message.reply_text(
        photo_text(u),
        reply_markup=make_keyboard_for_photo(u.bot_language)
    )

    return PHOTO


def add_photo(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    # update.message.reply_media_group(
    #     media=[
    #         InputMediaPhoto(media=update.message.photo[0].get_file().file_id)
    #     ]
    # )

    # print(update.message.photo[0].get_file().file_path)

    Media.objects.create(
        file_id=update.message.photo[0].get_file().file_id,
        user=u,
        media_type=Media.MediaType.PHOTO,
        is_main=not bool(u.media.count())
    )

    update.message.reply_text(
        photo_text(u),
        reply_markup=make_keyboard_for_photo(u.bot_language)
    )

    return PHOTO


def add_video(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    Media.objects.create(
        file_id=update.message.video.file_id,
        user=u,
        media_type=Media.MediaType.VIDEO,
        is_main=not bool(u.media.count())
    )

    update.message.reply_text(
        photo_text(u),
        reply_markup=make_keyboard_for_photo(u.bot_language)
    )

    return PHOTO


def add_file(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    update.message.reply_text(
        photo_text(u),
        reply_markup=make_keyboard_for_photo(u.bot_language)
    )

    return PHOTO


def save_photo(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    if update.message.text == BACK:
        update.message.reply_text(
            ENTER_LOCATION[u.bot_language],
            reply_markup=make_location_keyboard(u.bot_language)
        )

        return LOCATION
    elif update.message.text == ENOUGH_PHOTO:
        update.message.reply_text(
            ENTER_LOCATION[u.bot_language],
            reply_markup=make_location_keyboard(u.bot_language)
        )

        return LOCATION

    update.message.reply_text(
        photo_text(u),
        reply_markup=make_keyboard_for_photo(u.bot_language)
    )

    return PHOTO
