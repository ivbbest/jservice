from django.db import models


class Question(models.Model):
    id_question = models.IntegerField(unique=True)
    question = models.TextField(blank=True)
    answer = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True)

    def __str__(self):
        return self.question
