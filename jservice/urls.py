from django.contrib import admin
from django.urls import path

from parsing.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/questionlist/', QuestionAPIView.as_view()),
]
