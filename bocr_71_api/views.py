from django.shortcuts import render
from django.http import HttpResponse
from bocr_71_api.text_classifier.yolo.detect import detect
from bocr_71_api.text_classifier.helpers.classes import Recognizer
from bocr_71_api.constants import CHARACTER_CLASSIFIER_WEIGHT

def get_text(request):
    # if not request.GET: return
    return HttpResponse('HELLO')