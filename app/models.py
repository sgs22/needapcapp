from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = self.name.replace(' ', '-').lower()
        super().save(*args, **kwargs)
        

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.question
    
    def get_question_by_name(self, question):
        return self.objects.get(question=question)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.choice
    
class QuizResponse(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.quiz.name} - {self.user.username}'
    
    def get_quiz_response(quiz_id: int) -> 'QuizResponse':
        return QuizResponse.objects.get(quiz=quiz_id)
    
    def get_quiz_response_by_user(user_id: int) -> 'QuizResponse':
        return QuizResponse.objects.get(user=user_id)
    
    def get_latest_response(self) -> 'QuizResponse':
        return self.objects.latest(field_name=self.created_at)




