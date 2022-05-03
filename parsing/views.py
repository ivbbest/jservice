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

        # data, id_question = parser_questions(count)
        breakpoint()
        data = [{'id_question': 22955, 'question': 'This sitcom was well into its first season when Jaleel White joined it as Steve Urkel', 'answer': '<i>Family Matters</i>', 'created_at': '2014-02-11T22:59:31.086Z'}, {'id_question': 22956, 'question': 'This Teflon Don & Gambino Family boss spilled the beans on tape at the Ravenite Social Club in Manhattan', 'answer': 'John Gotti', 'created_at': '2014-02-11T22:59:31.108Z'}]

        id_question = [22955, 22956]

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
