from django.urls import path
from .views import generate_prompt

urlpatterns = [
    path('generate_prompt/', generate_prompt, name='generate_prompt'),
]
