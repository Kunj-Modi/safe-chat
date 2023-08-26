from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from .models import GlobalChat


@never_cache
@login_required(login_url="/login/")
def index(request):
    if request.method == "POST":
        user = request.user
        user_message = request.POST.get("user_message")
        if not user_message.strip() == "":
            message = GlobalChat.objects.create(user=user, user_message=user_message)
            return redirect("/global-chat/")
    chat = GlobalChat.objects.all().order_by("-message_time")[0:10]
    context = {"user_massage": chat}
    return render(request, "global_chat.html", context=context)


@never_cache
@login_required(login_url="/login/")
def messages(request):
    chat = GlobalChat.objects.all().order_by("-message_time")[0:10]
    results = []
    for message in chat:
        result = [str(request.user), str(message.user), str(message.user_message)]
        results.append(result)
    return JsonResponse(results, safe=False)