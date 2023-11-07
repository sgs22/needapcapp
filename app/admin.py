from django.contrib import admin

from app.models import Quiz, Question, Choice, QuizResponse

from django.contrib import admin
from app.models import Quiz, Question, Choice, QuizResponse

for model in [Quiz, Question, Choice, QuizResponse]:
    admin.site.register(model)
