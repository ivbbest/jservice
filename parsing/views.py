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

    id_question = map(lambda d: d['id_question'], data)

    return data, id_question


class QuestionsView(APIView):
    def post(self, request):
        i = 0
        count = request.data['questions_num']
        assert str(count).isnumeric(), "Don't correct questions_num. Repeat please!"
        # try:
        #
        #     count = request.data['questions_num']
        #     assert str(count).isnumeric(), "Don't correct Value"
        #
        #     print(type(count))
        #     print(str(count).isnumeric())
        # except json.decoder.JSONDecodeError as e:
        #     print("There was a problem accessing the equipment data.", e)
        # except ValueError as e:
        #     print('Dont correct parameter questions_num', e)
        # except TypeError as e:
        #     print('TypeError', e)
        # except Exception as e:
        #     print('Other Exception', e)

        data, id_question = parser_questions(count)
        for id in id_question:
            if Question.objects.filter(id_question=id).exist():
                i += 1

        if i > 0:
            data, id_question = parser_questions(i)

        serializer = QuestionSerializer(data=data, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
