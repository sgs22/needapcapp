from django import forms

#create a quiz form that init based on the quiz question
class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[question.question] = forms.ChoiceField(choices=[(choice.choice, choice.choice) for choice in question.choice_set.all()], widget=forms.RadioSelect(attrs={'class': 'text-blue-600'}))
