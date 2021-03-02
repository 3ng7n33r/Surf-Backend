from django.http import HttpResponse
import requests


def index(request):
    return HttpResponse("Hello, world")
