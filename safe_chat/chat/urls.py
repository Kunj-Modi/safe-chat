from django.urls import path, include
from . import views

urlpatterns = [
    path("messages/<str:sender_name>/", views.messages, name="messages"),
    path("<str:sender_name>", views.index, name="index"),
]
