import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

import tgbot.handlers.states.static_text
from tgbot.handlers.onboarding import static_text
from tgbot.handlers.states.handlers import send_profile, PROFILE
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.states.keyboards import make_keyboard_for_language


def command_start(update: Update, context: CallbackContext) -> int:
    u, created = User.get_user_and_created(update, context)

    if u.location_name is None or u.media.count() == 0:
        text = tgbot.handlers.states.static_text.CHOOSE_LANGUAGE[u.bot_language]

        update.message.reply_text(text=text,
                                  reply_markup=make_keyboard_for_language())

        return 0
    else:
        send_profile(update, u)

        return PROFILE


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )
