from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.states.keyboards import make_keyboard_for_sex, make_keyboard_for_language, make_keyboard_for_name, \
    make_keyboard_for_interest, make_location_keyboard, make_select_location_keyboard, make_keyboard_for_photo, \
    make_keyboard_for_description, make_keyboard_for_profile, make_keyboard_for_age
from tgbot.handlers.states.static_text import language_codes, CHOOSE_SEX, CHOOSE_LANGUAGE, MAN, WOMAN, ENTER_AGE, \
    ENTER_NAME, CHOOSE_INTEREST, BOYS, GIRLS, ALL, ENTER_LOCATION, NOT_FOUND_LOCATION, SElECT_LOCATION, SEND_PHOTO, \
    BACK, ENOUGH_PHOTO, ENTER_DESCRIPTION, SKIP, MY_PROFILE, CHANGE_MAIN, EDIT_PROFILE, CHOOSE_LANGUAGE_PROFILE, \
    SAVE_CURRENT, REMOVE_ALL_PHOTO, SAVE_CURRENT_DESC
from tgbot.locations.utils import search_place, get_place_name
from tgbot.models import User, Media

LANGUAGE, SEX, AGE, NAME, LOCATION, INTEREST, SELECT_LOCATION, PHOTO, DESCRIPTION, PROFILE = range(10)


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
            reply_markup=make_keyboard_for_age(u)
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
            ENTER_AGE[u.bot_language],
            reply_markup=make_keyboard_for_age(u)
        )

        return AGE


def set_name(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    name = update.message.text[:30]
    u.name = name
    u.save()

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
            reply_markup=make_location_keyboard(u.bot_language, exists=u.location_name is not None)
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

    if update.message.text == SAVE_CURRENT[u.bot_language]:
        update.message.reply_text(
            photo_text(u),
            reply_markup=make_keyboard_for_photo(u.bot_language, first=not bool(u.media.count()))
        )

        return PHOTO

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
            reply_markup=make_location_keyboard(u.bot_language, exists=u.location_name is not None)
        )

        return LOCATION


def select_location(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    for candidate in context.user_data['location_candidates']:
        if f"{candidate['name']} ({candidate['formatted_address']})" == update.message.text:
            u.location_lat = candidate['geometry']['location']['lat']
            u.location_lon = candidate['geometry']['location']['lng']
            u.location_name = get_place_name(u.location_lat, u.location_lon)
            u.save()

            update.message.reply_text(
                photo_text(u),
                reply_markup=make_keyboard_for_photo(u.bot_language, first=not bool(u.media.count()))
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

    u.location_name = get_place_name(lat, lon)
    u.save()

    update.message.reply_text(
        photo_text(u),
        reply_markup=make_keyboard_for_photo(u.bot_language, first=not bool(u.media.count()))
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
        link=context.bot.get_file(update.message.photo[0].get_file().file_id)['file_path'],
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
        link=context.bot.get_file(update.message.video.file_id)['file_path'],
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

    if update.message.text == BACK[u.bot_language]:
        update.message.reply_text(
            ENTER_LOCATION[u.bot_language],
            reply_markup=make_location_keyboard(u.bot_language, exists=u.location_name is not None)
        )

        return LOCATION
    elif update.message.text == ENOUGH_PHOTO[u.bot_language]:
        update.message.reply_text(
            ENTER_DESCRIPTION[u.bot_language],
            reply_markup=make_keyboard_for_description(u.bot_language, exists=u.description != "")
        )

        return DESCRIPTION

    elif update.message.text == REMOVE_ALL_PHOTO[u.bot_language]:
        u.media.all().delete()

    update.message.reply_text(
        photo_text(u),
        reply_markup=make_keyboard_for_photo(u.bot_language, first=not bool(u.media.count()))
    )

    return PHOTO


def profile_text(user: User) -> str:
    return MY_PROFILE[user.bot_language].format(
        name=user.name,
        years=user.age,
        place=user.location_name,
        description=" - " + user.description if user.description != "" else ""
    )


def send_profile(update: Update, u: User):
    media = u.media.filter(is_main=True).first()

    if media is None:
        media = u.media.first()

    if media.media_type == Media.MediaType.PHOTO:
        update.message.reply_photo(
            caption=profile_text(u),
            photo=media.file_id,
            reply_markup=make_keyboard_for_profile(u)
        )
    else:
        update.message.reply_video(
            caption=profile_text(u),
            video=media.file_id,
            reply_markup=make_keyboard_for_profile(u)
        )


def save_description(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    if update.message.text == SKIP[u.bot_language]:
        u.description = ""
    elif update.message.text == SAVE_CURRENT_DESC[u.bot_language]:
        pass
    elif update.message.text == BACK[u.bot_language]:
        update.message.reply_text(
            photo_text(u),
            reply_markup=make_keyboard_for_photo(u.bot_language)
        )

        return PHOTO
    else:
        u.description = update.message.text[:512]

    u.save()

    send_profile(update, u)

    return PROFILE


def profile_funcs(update: Update, context: CallbackContext):
    u = User.get_user(update, context)

    if update.message.text == CHANGE_MAIN[u.bot_language]:
        photos: list[Media] = list(u.media.all())

        main_index = 0
        photo_count = len(photos)

        for i in range(photo_count):
            if photos[i].is_main:
                photos[i].is_main = False
                photos[i].save()
                main_index = i
                break

        photos[(main_index + 1) % photo_count].is_main = True
        photos[(main_index + 1) % photo_count].save()

        send_profile(update, u)
    elif update.message.text == EDIT_PROFILE[u.bot_language]:
        update.message.reply_text(text=CHOOSE_LANGUAGE_PROFILE[u.bot_language],
                                  reply_markup=make_keyboard_for_language())

        return LANGUAGE
