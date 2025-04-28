from django.urls import path
from .views import generate_prompt

urlpatterns = [
    path('generate/', generate_prompt),
]
