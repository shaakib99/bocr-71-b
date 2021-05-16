from django.http import JsonResponse
from bocr_71_api.classifier_helper.classifier import get_text_from_image
from django.views.decorators.csrf import csrf_exempt
from .view_helper import generate_random_name
import json
import base64
import cv2


@csrf_exempt
def get_text(request):
    data = json.loads(request.body)
    if not data or data.get('blobImg') == None: return JsonResponse({'status': '400'})

    decodable_data = data['blobImg'][22:]
    filename = f'bocr_71_api/test/{generate_random_name()}.png'

    with open(filename, 'wb') as f:
        f.write(base64.b64decode(decodable_data))

    img = cv2.imread(filename)
    img = cv2.GaussianBlur(img,(3,3),0)
    cv2.imwrite(filename, img)

    text = get_text_from_image(image_src=filename)

    return JsonResponse({'status': '200', 'text':text})