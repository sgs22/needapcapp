from django.test import TestCase
from django.urls import reverse
from app.models import Quiz, QuizResponse, User



class AppViewsTest(TestCase):

    def test_index_response(self):
        index = self.client.get(reverse('index'))
        response = index.status_code
        self.assertEquals(response, 200)


class QuizResponseModelTest(TestCase):
    def setUp(self) -> None:
        self.quiz = Quiz.objects.create(name='Test Quiz', description='Test Quiz Description')
        self.user = User.objects.create_user('test_user', '', 'test_password')
        self.quiz_response = QuizResponse.objects.create(quiz_id=self.quiz.pk, user_id=self.user.pk, response={'question_1': 'choice_1'})

    def test_quiz_response_has_user(self):
        self.assertEquals(self.quiz_response.user.pk, 1)

    def test_quiz_response_has_quiz(self):
        self.assertEquals(self.quiz_response.quiz.pk, 1)

    def text_quiz_response_response_is_valid_json(self):
        self.assertEquals(self.quiz_response.response, {'question_1': 'choice_1'})

    