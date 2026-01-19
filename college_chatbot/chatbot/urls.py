from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot_ui, name="chatbot"),
    path("get/", views.chat_response, name="chat_response"),
    path("analytics/", views.analytics, name="analytics"),
]

