from .views import *
from django.urls import path


urlpatterns = [
    path('api/v1/question/', QuestionsView.as_view()),
]
