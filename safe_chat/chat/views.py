import time
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from chat_list.models import Chat, Message


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url="/login/"), name='dispatch')
class Index(View):
    def get(self, request, other):
        user = request.user
        sender = User.objects.get(username=other)
        try:
            chat_id = Chat.objects.get(Q(user1=user.id, user2=sender.id) | Q(user1=sender.id, user2=user.id)).chat_id
        except Exception as e:
            new_chat = Chat.objects.create(user1=user, user2=sender, last_message=datetime.now())
            chat_id = new_chat.chat_id
        messages = Message.objects.filter(chat_id=chat_id).order_by("message_time")
        if messages.count() > 30:
            ids_to_keep = messages.order_by("-message_time")[:messages.count() - 10].values_list("id", flat=True)
            Message.objects.exclude(id__in=ids_to_keep).delete()

        context = {"all_messages": messages, "sender_name": other}
        return render(request, "chat.html", context=context)

    def post(self, request, other):
        user = request.user
        sender = User.objects.get(username=other)
        chat_id = Chat.objects.get(Q(user1=user.id, user2=sender.id) | Q(user1=sender.id, user2=user.id))
        user_message = request.POST.get("user_message").strip()
        chat_id.last_message = datetime.now()
        chat_id.save()
        if user_message != "":
            Message.objects.create(chat_id=chat_id, from_user=user, message=user_message)
        return redirect(f"/chat/{other}")
