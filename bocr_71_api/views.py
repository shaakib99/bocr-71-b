from django.http import HttpResponse, JsonResponse
from bocr_71_api.classifier_helper.classifier import get_text_from_image

def get_text(request):
    # if not request.GET: return
    print(get_text_from_image(image_src='bocr_71_api/test.png'))

    return HttpResponse('Done')