from django.urls import path, include
from . import views

urlpatterns = [
    path("<str:other>", views.Index.as_view(), name="index"),
]
