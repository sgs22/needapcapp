import uuid
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from app.models import Choice, Question, Quiz, QuizResponse
from app.forms import QuizForm

# import anonymous user from django
from django.contrib.auth.models import User


# create class index view
class IndexView(View):
    def get(self, request):
        return render(request, 'app/index.html')


#create a form view that will show a form that will allow a user to answer questions from the quix based on the choices
# open detail view based on slug url
class QuizView(DetailView):
    model = Quiz
    template_name = 'app/quiz_form.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return Quiz.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuizForm(questions=Question.objects.filter(quiz=self.object))
        context['questions'] = Question.objects.filter(quiz=self.object)
        context['choices'] = Choice.objects.filter(question__quiz=self.object)
        return context
    
    def get_anonymous_user(self):
        try:
            return User.objects.get(username='anonymous')
        except User.DoesNotExist as e:
            return None
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            anon_user = self.get_anonymous_user()
            if not anon_user:
                default_pw = str(uuid.uuid4())
                anon_user = User.objects.create_user('anonymous', '', default_pw)
            quiz_response_user = anon_user
        else: 
            quiz_response_user = request.user
        quiz_response_data = request.POST.copy()
        quiz_response_object = QuizResponse.objects.create(
            quiz=self.get_object(),
            user=quiz_response_user,
            response=quiz_response_data
        )
        context = {'quiz_response': quiz_response_object}
        return render(request, 'app/quiz_response.html', context)
    
#create class view to present the quiz response
class QuizResponseView(DetailView):
    model = QuizResponse
    template_name = 'app/quiz_response.html'

    def get_object(self):
        quiz_slug = self.kwargs.get('quiz_slug')
        user_id = self.kwargs.get('user_id')
        return QuizResponse.objects.get(quiz__slug=quiz_slug, user__id=user_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_name'] = self.get_object().quiz.name
        return context