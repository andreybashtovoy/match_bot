import random
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from dtb.settings import DEBUG, TELEGRAM_TOKEN

from tgbot.models import User
from tgbot.forms import BroadcastForm

from tgbot.tasks import broadcast_message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name', 
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']

    def invited_users(self, obj):
        return obj.invited_users().count()

    def broadcast(self, request, queryset):
        if 'apply' in request.POST:
            broadcast_message_text = request.POST["broadcast_text"]

            # TODO: for all platforms?
            if len(queryset) <= 3 or DEBUG:  # for test / debug purposes - run in same thread
                for u in queryset:
                    u.send_message(broadcast_message_text)
                self.message_user(request, "Just broadcasted to %d users" % len(queryset))
            else:
                user_ids = list(set(u.user_id for u in queryset))
                random.shuffle(user_ids)
                broadcast_message.delay(message=broadcast_message_text, user_ids=user_ids)
                self.message_user(request, "Broadcasting of %d messages has been started" % len(queryset))

            return HttpResponseRedirect(request.get_full_path())

        form = BroadcastForm(initial={'_selected_action': queryset.values_list('user_id', flat=True)})
        return render(
            request, "admin/broadcast_message.html", {'items': queryset,'form': form, 'title':u' '}
        )