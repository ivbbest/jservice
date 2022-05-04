from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Стандартный сериализатор для сериализации данных
    """
    class Meta:
        model = Question
        fields = '__all__'
