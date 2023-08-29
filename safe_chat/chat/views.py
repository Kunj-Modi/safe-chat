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
    try:
        time_diff = received[0].message_time - sent[0].message_time
    except IndexError:
        time_diff = 0
    context = {"sent": sent, "received": received, "time_diff": time_diff, "sender_name": sender_name}
    return render(request, "chat.html", context=context)


@never_cache
@login_required(login_url="/login/")
def messages(request, sender_name):
    user_name = request.user
    user_id = User.objects.get(username=user_name).id
    sender_id = User.objects.get(username=sender_name).id
    sent_query = ChatList.objects.filter(messageTo=user_id).filter(messageFrom=sender_id)
    received_query = ChatList.objects.filter(messageTo=sender_id).filter(messageFrom=user_id)
    try:
        time_diff = received_query[0].message_time - sent_query[0].message_time
    except IndexError:
        time_diff = 0
    received = []
    sent = []
    for chat in received_query:
        received.append(str(chat.user_message))
    for chat in sent_query:
        sent.append(str(chat.user_message))
    results = [{"received": received, "sent": sent, "time_diff": time_diff}]
    return JsonResponse(results, safe=False)
