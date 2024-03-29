from django import forms


class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for i, question in enumerate(questions):
            self.fields[question.question] = forms.ChoiceField(
                choices=[(choice.choice, choice.choice)
                         for choice in question.choice_set.all()],
                widget=forms.RadioSelect(
                    attrs={'class': 'text-2xl', 'id': f'question_{i}'}),

            )
