from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('content', 'document')

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(FeedbackForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(FeedbackForm, self).save(commit=False)
        inst.author = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst
