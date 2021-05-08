from django.shortcuts import render
from django.http import HttpResponse

def get_text(request):
    # if not request.GET: return
    return HttpResponse('HELLO')