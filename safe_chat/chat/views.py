from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required(login_url="/login/")
def index(request):
    return HttpResponse("Chat")
