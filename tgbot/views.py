import json
import logging

import requests
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, FileResponse, HttpResponse

from dtb.settings import DEBUG
from tgbot.dispatcher import process_telegram_event, bot
from tgbot.models import User, Media

logger = logging.getLogger(__name__)


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again. 
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)! 
            # Read Procfile for details
            # You can run all of these services via docker-compose.yml
            process_telegram_event.delay(json.loads(request.body))

        # TODO: there is a great trick to send action in webhook response
        # e.g. remove buttons, typing event
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})


def file_view(request, user_id, file_id):
    media = Media.objects.filter(file_id=file_id).first()

    file = requests.get(media.link).content

    return HttpResponse(file, content_type="image/jpeg")


def profile_view(request, user_id):
    user = User.objects.get(pk=user_id)

    photo_links = [(obj.file_id, obj.media_type) for obj in user.media.all()]

    return render(request, 'profile/base.html', context={'photo_links': photo_links})
