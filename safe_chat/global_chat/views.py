from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from .models import GlobalChat


@never_cache
@login_required(login_url="/login/")
def index(request):
    chat = GlobalChat.objects.all().order_by("message_time")
    if GlobalChat.objects.count() > 100:
        ids_to_keep = GlobalChat.objects.order_by("-message_time")[:GlobalChat.objects.count() - 40].values_list("id", flat=True)
        GlobalChat.objects.exclude(id__in=ids_to_keep).delete()
    context = {"user_massage": chat}
    return render(request, "global_chat.html", context=context)
