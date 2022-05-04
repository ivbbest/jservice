from .models import Question
from .serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests


URL = 'https://jservice.io/api/random?count='


def parser_questions(count):
    """
    Парсинг данных из 'https://jservice.io/api/random?count=' по заданному count
    """

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


class QuestionView(APIView):
    """
    Вьюшка для Question
    """
    def post(self, request):
        count = request.data['questions_num']

        # проверка, что задано целое число count, иначе вывод ошибки
        if not isinstance(count, int):
            raise ValueError("Don't correct questions_num. Repeat please!")

        # вызов функции парсинга
        data, id_question = parser_questions(count)

        # поиск одинаковых вопросов
        same_questions = Question.objects.filter(id_question__in=id_question).count()

        # если есть одинаковые вопросы, то запускаем цикл, чтобы парсить новые вопросы
        # пока не будет достигнута уникальность
        while same_questions > 0:
            data_new, id_question_new = parser_questions(same_questions)
            data += data_new
            same_questions = Question.objects.filter(id_question__in=id_question_new).count()

        # передаем все на вход сериализатору
        serializer = QuestionSerializer(data=data, many=True)

        # проверка валидации и сохранение в базу
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # Ответ на запрос, который должен быть предыдущей сохранённый вопрос для викторины.
            # В случае его отсутствия - пустой объект.
            previous_item_id = Question.objects.last().id-1

            if not Question.objects.filter(id=previous_item_id).exists():
                response = {'question_text': None}
                return Response(response, status=status.HTTP_200_OK)

            last_obj = Question.objects.filter(id=previous_item_id).values('question')
            response = {'question_text': last_obj}

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
