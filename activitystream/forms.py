from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'document')

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(CommentForm, self).save(commit=False)
        inst.author = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst



