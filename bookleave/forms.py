from django import forms
from .models import Leave, Reply
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['type', 'begindate', 'enddate', 'document', 'title', 'content']
        widgets = {
            'begindate': forms.DateInput(attrs={'type': 'date', 'style': 'max-width: 12em'}),
            'enddate': forms.DateInput(attrs={'type': 'date', 'style': 'max-width: 12em'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if 'begindate' in cleaned_data.keys():
            begindate = cleaned_data['begindate']
        else:
            begindate = None
            raise ValidationError('wrong initials')
        if 'enddate' in cleaned_data.keys():
            enddate = cleaned_data['enddate']
        else:
            enddate = None
            raise ValidationError('wrong initials')

        if begindate < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0):
            raise ValidationError('Begin date can not be past from today')

        if enddate < begindate:
            raise ValidationError('End date can not be earlier than beginning date')

        if enddate == begindate:
            raise ValidationError('Begin date and end date can not be the same day')

        leaves = Leave.objects.filter(owner=self.user).all()
        # current_one = Leave.objects.get(owner=self.user, pk=self.object.pk)
        for leave in leaves:
            if begindate == leave.begindate:
                raise ValidationError('There is an existing report between these days')
            elif enddate == leave.enddate:
                raise ValidationError('There is an existing report between these days')
            elif begindate > leave.begindate and begindate < leave.enddate:
                raise ValidationError('There is an existing report between these days')
            elif begindate < leave.begindate and enddate > leave.enddate:
                raise ValidationError('There is an existing report between these days')
            elif begindate < leave.begindate and enddate > leave.begindate and enddate < leave.enddate:

                raise ValidationError('There is an existing report between these days')


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['type', 'begindate', 'enddate', 'document', 'title', 'content']
        widgets = {
            'begindate': forms.DateInput(attrs={'type': 'date', 'style': 'max-width: 12em'}),
            'enddate': forms.DateInput(attrs={'type': 'date', 'style': 'max-width: 12em'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.object = kwargs.pop('current_leave')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if 'begindate' in cleaned_data.keys():
            begindate = cleaned_data['begindate']

        else:
            begindate = None
            raise ValidationError('wrong initials')
        if 'enddate' in cleaned_data.keys():
            enddate = cleaned_data['enddate']
        else:
            enddate = None
            raise ValidationError('wrong initials')

        if begindate < timezone.now().replace(hour=0, minute=0, second=0, microsecond=0):
            raise ValidationError('Begin date can not be earlier than current day')

        if enddate < begindate:
            raise ValidationError('End date can not be earlier than beginning date')

        if enddate == begindate:
            raise ValidationError('Begin date and end date can not be the same day')

        leaves = Leave.objects.filter(owner=self.user).all()
        current_one = Leave.objects.get(owner=self.user, pk=self.object.pk)

        for leave in leaves:
            if leave.pk == current_one.pk:
                continue
            if begindate == leave.begindate:
                raise ValidationError('There is an existing report between these days')
            elif enddate == leave.enddate:
                raise ValidationError('There is an existing report between these days')
            elif begindate > leave.begindate and begindate < leave.enddate:
                raise ValidationError('There is an existing report between these days')
            elif begindate < leave.begindate and enddate > leave.enddate:
                raise ValidationError('There is an existing report between these days')
            elif begindate < leave.begindate and enddate > leave.begindate and enddate < leave.enddate:
                raise ValidationError('There is an existing report between these days')


class AcceptorReject(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['is_accepted', 'is_rejected']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_accpeted = cleaned_data['is_accepted']
        is_rejected = cleaned_data['is_rejected']

        if is_accpeted == True and is_rejected == True:
            raise ValidationError('You must select only one checkbox!')
        if is_accpeted == False and is_rejected == False:
            raise ValidationError('You must select only one checkbox!')


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ReplyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(ReplyForm, self).save(commit=False)
        inst.owner = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


