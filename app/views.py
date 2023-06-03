from django.shortcuts import render
from django.views.generic import DetailView
from app.models import Choice, Question, Quiz
from app.forms import QuizForm

# Create your views here.
# create a view that will show a quiz based on a slug
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quiz=self.object)
        context['choices'] = Choice.objects.filter(question__quiz=self.object)
        return context
    
#create a form view that will show a form that will allow a user to answer questions from the quix based on the choices
# open detail view based on slug url
class QuizFormView(DetailView):
    model = Quiz
    template_name = 'quiz_form.html'

    #add a form to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuizForm()
        context['questions'] = Question.objects.filter(quiz=self.object)
        context['choices'] = Choice.objects.filter(question__quiz=self.object)
        return context
    
    #create a post method that will process the form data
    def post(self, request, *args, **kwargs):
        data = request.POST
        #create a variable to hold the score