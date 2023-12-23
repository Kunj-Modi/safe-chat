from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from .models import Chat


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required(login_url="/login/"), name='dispatch')
class Index(View):
    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(Q(user1=user) | Q(user2=user)).order_by("-last_message")
        new_chats = []
        for chat in chats:
            name = chat.user1 if chat.user2 == user else chat.user2
            new_chats.append(name)
        context = {"chats": new_chats}
        return render(request, "chat_list.html", context=context)

    def post(self, request):
        search = request.POST.get("search")
        if User.objects.filter(username=search).exists() and not request.user.username == search:
            return redirect(f"/chat/{search}")
        else:
            return render(request, "chat_list.html", context={"chats": []})
