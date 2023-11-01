from django.test import TestCase
from django.urls import reverse
from app.models import Quiz



class NeedapcTestCase(TestCase):
    def test_index_response(self):
        index = self.client.get(reverse('index'))
        response = index.status_code
        self.assertEquals(response, 200)



class NeedapcQuizModelTestCase(TestCase):
    def setUp(self):
        self.model_test_quiz_instance = Quiz.objects.create(name='Test Quiz', description='Test Quiz Description')

    def test_quiz_model_has_slug(self):
        self.assertEquals(self.model_test_quiz_instance.slug, 'test-quiz')