from django.urls import path
from .views import generate_prompt, check_status

urlpatterns = [
    path('generate_prompt/', generate_prompt, name='generate_prompt'),
    path('check_status/<str:request_id>/', check_status, name='check_status'),
]