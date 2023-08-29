from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("chat_list.urls"), name="chat_list"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_page, name="logout"),
    path('chat/', include("chat.urls"), name="chat"),
    path('chat-list/', include("chat_list.urls"), name="chat_list"),
    path('global-chat/', include("global_chat.urls"), name="global_chat"),
]
