import json

from django.http import Http404
from django.shortcuts import render
from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests


URL = 'https://jservice.io/api/random?count='


def parser_questions(count):
    api_url = f'{URL}{count}'
    response_data = requests.get(api_url).json()
    data = [
        {
            'id_question': res['id'],
            'question': res['question'],
            'answer': res['answer'],
            'created_at': res['created_at'],

        }
        for res in response_data
    ]

    id_question = list()

    for d in data:
        id_question.append(d['id_question'])

    return data, id_question


class QuestionsView(APIView):
    def post(self, request):
        count = request.data['questions_num']

        if not isinstance(count, int):
            raise ValueError("Don't correct questions_num. Repeat please!")

        data, id_question = parser_questions(count)
        same_questions = Question.objects.filter(id_question__in=id_question).count()

        while same_questions > 0:
            data_new, id_question_new = parser_questions(same_questions)
            data += data_new
            same_questions = Question.objects.filter(id_question__in=id_question_new).count()

        serializer = QuestionSerializer(data=data, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
