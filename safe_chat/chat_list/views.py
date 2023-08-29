from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from .models import ChatList


@never_cache
@login_required(login_url="/login/")
def index(request):
    user = request.user
    chats = ChatList.objects.filter(messageTo=user).order_by("-message_time").values("messageFrom")
    new_chats = []
    for chat in chats:
        name = User.objects.filter(pk=chat["messageFrom"])[0]
        if name not in new_chats:
            new_chats.append(name)
    context = {"chats": new_chats}
    return render(request, "chat_list.html", context=context)


@never_cache
@login_required(login_url="/login/")
def messages(request):
    user = request.user
    chats = ChatList.objects.filter(messageTo=user).order_by("-message_time").values("messageFrom")
    results = []
    for chat in chats:
        name = User.objects.filter(pk=chat["messageFrom"])[0]
        if str(name) not in results:
            results.append(str(name))
    return JsonResponse(results, safe=False)
