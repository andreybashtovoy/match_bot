from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [  
    # TODO: make webhook more secure
    path('', views.index, name="index"),
    path('profile/<int:user_id>/', views.profile_view, name="profile"),
    path('profile/<int:user_id>/<str:file_id>', views.file_view, name="file"),
    path('super_secter_webhook/', csrf_exempt(views.TelegramBotWebhookView.as_view())),
]
