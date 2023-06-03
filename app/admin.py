from django.contrib import admin

# Register your models here.
from app.models import Quiz, Question, Choice, QuizResponse

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizResponse)
