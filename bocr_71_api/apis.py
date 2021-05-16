from django.urls import path
from bocr_71_api import views
urlpatterns = [
    path('get_text/', views.get_text, name='get_image_to_text'),
]
