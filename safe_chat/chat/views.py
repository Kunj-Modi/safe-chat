from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from chat_list.models import ChatList


@never_cache
@login_required(login_url="/login/")
def index(request, sender_name):
    user_name = request.user
    user_id = User.objects.get(username=user_name).id
    sender_id = User.objects.get(username=sender_name).id
    sent = ChatList.objects.filter(messageTo=user_id).filter(messageFrom=sender_id)
    received = ChatList.objects.filter(messageTo=sender_id).filter(messageFrom=user_id)
    all_messages = (sent | received).order_by("message_time")
    context = {"all_messages": all_messages, "sender_name": sender_name}
    return render(request, "chat.html", context=context)


@never_cache
@login_required(login_url="/login/")
def messages(request, sender_name):
    user_name = request.user
    user_id = User.objects.get(username=user_name).id
    sender_id = User.objects.get(username=sender_name).id
    sent_query = ChatList.objects.filter(messageTo=user_id).filter(messageFrom=sender_id)
    received_query = ChatList.objects.filter(messageTo=sender_id).filter(messageFrom=user_id)
    messages_query = (sent_query | received_query).order_by("message_time")
    all_messages = []
    for chat in messages_query:
        all_messages.append([str(chat.messageTo), str(chat.user_message)])
    return JsonResponse(all_messages, safe=False)
