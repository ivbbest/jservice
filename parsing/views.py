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

    return data


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

        data = parser_questions(count)
        serializer = QuestionSerializer(data=data, many=True)

        breakpoint()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, id_question):
        try:
            return Question.objects.get(id_question=id_question)
        except Question.DoesNotExist:
            raise Http404

# @api_view(['POST'])
# def questions_list(request):
#     try:
#         count = request.data['questions_num']
#
#         print(count)
#     except json.decoder.JSONDecodeError as e:
#         print("There was a problem accessing the equipment data.", e)
#     except ValueError as e:
#         print('Dont correct parameter questions_num', e)
#     except TypeError as e:
#         print('TypeError', e)
#     except Exception as e:
#         print('Other Exception', e)
#
#
#
#
#
# '''
# @api_view(['GET', 'POST'])
# def questions_list(request):
#     if request.method == 'POST':
#         try:
#             count = request.data['questions_num']
#             api_url = f'{URL}{count}'
#             response_data = requests.get(api_url).json()
#             data = [
#                 {
#                     "id_question": res['id'],
#                     "question": res['question'],
#                     "answer": res['answer'],
#                     "created_at": res['created_at'],
#
#                 }
#                 for res in response_data
#             ]
#
#             serializer = QuestionSerializer(data=data, many=True)
#
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 print(data)
#
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except json.decoder.JSONDecodeError as e:
#             print("There was a problem accessing the equipment data.", e)
#         except ValueError as e:
#             print('Dont correct parameter questions_num', e)
#         except TypeError as e:
#             print('TypeError', e)
#         except Exception as e:
#             print('Other Exception', e)
# '''
#
#         # return Response(data=serializer.data)
#         # # serializer = SnippetSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # class QuestionAPIView(generics.ListCreateAPIView):
# #     # queryset = Question.objects.all()
# #     serializer_class = QuestionSerializer
# #
# #     # def get_queryset(self):
# #     # #     info = self.request.data['questions_num']
# #     #     return Response({"message": "Got some data!", "data": request.data})
# #
# #     def post(self, request, *args, **kwargs):
# #         count = request.data['questions_num']
# #         # breakpoint()
# #         api_url = f'{URL}{count}'
# #         response_data = requests.get(api_url).json()
# #         print(response_data)
# #         return Response({'Status': 'OK'})
# #         # return Response({"message": "Got some data!", "data": request.data})
# #
# # # class QuestionAPIView(APIView):
# # #     def get(self, request):
# # #         return Response({'title': 'Angelina Jolie'})
# # #
# # #     def post(self, request):
# # #         # return Response({'title': 'Jennifer Shrader Lawrence'})
# # #         info = self.request.data['questions_num']
# # #         return Response({'post': model_to_dict(info)})
