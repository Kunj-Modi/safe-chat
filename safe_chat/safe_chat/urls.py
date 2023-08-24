from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_page, name="logout"),
]
