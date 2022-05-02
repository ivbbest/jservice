from django.shortcuts import render
from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer


class QuestionAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
