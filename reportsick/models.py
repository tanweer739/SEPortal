from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required


# Create your models here.

class Report(models.Model):
    title = models.TextField(max_length=100)
    content = models.TextField()
    document = models.FileField(blank=True, default=None, upload_to='documents')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reports-home')

    @property
    def filename(self):
        return os.path.basename(self.document.path)

    @property
    def feedbackunseenStaff(self):
        number = self.feedback_set.filter(author=self.author_id, is_seen=False).count()
        return number

    @property
    def feedbackunseenActive(self):
        number = self.feedback_set.filter(~Q(author=self.author_id), is_seen=False).count()
        return number


class Feedback(models.Model):
    content = models.TextField()
    document = models.FileField(blank=True, default=None, upload_to='documents')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, default=None)
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('report-detail', kwargs={'pk': self.report_id})

    @property
    def filename(self):
        return os.path.basename(self.document.path)

    @property
    def feedbackseen(self):
        temp = Feedback.objects.get(pk=self.pk)
        print(temp)
        temp.is_seen = True
        temp.save()
