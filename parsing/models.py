from django.db import models
 
 
class Question(models.Model):
	id_question = models.IntegerField(unique=True)
	question = models.TextField(blank=True)
	answer = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)

 
	def __str__(self):
		return self.question
